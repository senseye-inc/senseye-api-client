import subprocess as sp
from pathlib import Path
import time
import yaml
from senseye_api_client.utils import deep_merge
from logging import getLogger
import sys

from . docker import TEST_LABEL
from . config import SUBPROCESS_LOGS

log = getLogger(__name__)

VERSION = "3.3"


class DockerComposer():
    '''
    Tool to construct Docker Compose Stacks With variable entries
    Example:
        stack = DockerComposer()
        stack.add_service('mongodb', image='mongo', ports=['27017:27017'])
        stack.add_service('redis', image='redis')
        stack.start(logs=['mongodb'])
        stack.stop()
    '''

    def __init__(self,
                 file_name='build/docker-compose.yaml',
                 project_name=TEST_LABEL,
                 network_name=TEST_LABEL,
                 label=TEST_LABEL
                ):
        self.file = Path(file_name).absolute()
        self.file.parent.mkdir(exist_ok=True, parents=True)
        self.network = network_name
        self.label = label
        self.proc = None
        self.name = project_name

        # Initial Config
        self.config = {
            "services": {},
            "version": VERSION,
            "networks": {
                network_name: {
                    'external': {
                        'name': network_name,
                    }
                }
            }
        }

    def run_cmd(self, args):
        PIPE = None if SUBPROCESS_LOGS else sp.DEVNULL
        return sp.Popen(
            f'docker-compose -p {self.name} -f {self.file} {args}'.split(' '),
            stdout=PIPE, stderr=PIPE
        )

    def start(self, exclude=None, include=None, logs='all'):
        # Make sure logs is a string
        if type(logs) is list:
            logs = ' '.join(logs)

        # Copy the config, as it will be mutated
        config = deep_merge(self.config, {})

        if include:
            [config.pop(name) for name in self.config['services'] if name not in include]

        elif exclude:
            [config.pop(name, '') for name in exclude]

        # Write out the yaml file to use for docker-compose
        with open(self.file, 'w') as f:
            yaml.dump(self.config, f)

        try:
            sp.Popen(f'docker network create {self.network} --attachable'.split(' ')).wait()
            log.info(f'Network {self.network} Created')
        except sp.CalledProcessError:
            log.info('Network not created; probably already exists')

        # Start up all with a blocking call
        self.run_cmd(f'up -d').wait()

        if not logs:
            self.proc = None

        # Special case for all
        elif logs == 'all':
            # Attach to the logs with a running process
            self.proc = self.run_cmd(f'logs -f --tail=all')

        # Otherwise just show the requested logs
        else:
            self.proc = self.run_cmd(f'logs -f --tail=all {logs}')

        # Arbitrary time to wait
        time.sleep(5)

    def add_service(self, name, service_spec={}, **kwargs):
        config = {**service_spec, **kwargs}
        # Merge with default
        config = deep_merge(config, {
            'networks': [],
            'labels': {}
        })

        # add netowrk and label
        config['networks'].append(self.network)
        config['labels'][self.label] = ''

        # Add to config
        self.config['services'][name] = config

    def add_services(self, services):
        for service_name, config in services.items():
            self.add_service(service_name, config)

    def add_mount(self, service, mount_point, mount_target):
        '''
        Mount a Location for debugging purposes
        '''
        log.warning(f"Mount Point being used: ({service}) {mount_point}:{mount_target}, use for DEBUGGING only")

        mount_point = Path(mount_point).absolute()
        self.config['services'][service].setdefault('volumes', [])
        self.config['services'][service]['volumes'].append(f'{mount_point}:{mount_target}')

    def stop(self, timeout=10):
        log.info('Shutting down stack')

        if self.proc is not None:
            # Kill log process if still running
            try:
                self.proc.kill()
            except Exception as e:
                log.info(f"Exception Killing Process: {e}")

        # Turn off gracefully
        try:
            self.run_cmd(f'down --remove-orphans').wait(1)
        except sp.TimeoutExpired:
            log.info('Stopping Process Timed out, force killing')

            # Force Shutdown
            try:
                self.run_cmd(f'kill').wait(5)
            except Exception as e:
                log.warning(f'Killing Process failed: {e}')

    def __del__(self):
        try:
            # Frequently runs into error
            # because this is called as python is shutting down
            self.stop()
        except Exception:
            pass
