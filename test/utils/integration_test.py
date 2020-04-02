import unittest
import time
from logging import getLogger

from senseye_api_client.utils import deep_merge

from . config import TAG, DOCKER_LOGS
from . docker_composer import DockerComposer


log = getLogger(__name__)


class IntegrationTest(unittest.TestCase):
    """
    IntegrationTest is a test framework that starts up services and mocks, and
    gives access to the gRPC stubs that they create
    Example:

        >>> class MyClass(IntegrationTest):
        >>>     SERVICES = ['compute']
        >>>     MOCKS = {'storage': 'StorageMock'}
        >>>     TAG = 'latest'
        >>>     CONFIG = {'hosts': {'cluster_scheduler': 'localhost:8786'}}
        >>>
        >>>     def my_test(self):
        >>>        with self.stubs['compute'] as stub1:
        >>>            stub1.Function()
        >>>
        >>>        with self.stubs['storage'] as stub2:
        >>>            stub2.Function()
    """

    # Dictionary of services and their implemntations
    TAG = TAG

    GRPC_PORT = 50020
    RABBITMQ_DASHBOARD_PORT = 20101
    FLOWER_PORT = 20102
    DASK_DASHBOARD_PORT = 20103

    # Extra containers to run with test
    CONTAINERS = {
        'gateway': {
            'image': 'senseyeinc/eucalyptus:gateway-${TAG:-latest}',
            'ports': [f'{GRPC_PORT}:50020']
        },
        'compute': {
            'image': 'senseyeinc/eucalyptus:compute-${TAG:-latest}'
        },
        'rabbitmq': {
            'image': 'rabbitmq:3-management',
            'ports': [f'{RABBITMQ_DASHBOARD_PORT}:15672']
        },
        'mongodb': {
            'image': 'mongo'
        },
        'compute-tasks': {
            'image': 'senseyeinc/eucalyptus:compute-tasks-${TAG:-latest}',
            'depends_on': ['rabbitmq', 'mongodb'],
        },
        'flower': {
            'image': 'mher/flower',
            'command': 'celery flower --broker=amqp://rabbitmq:5672 --address=0.0.0.0 --port=5555',
            'ports': [f'{FLOWER_PORT}:5555'],
            'depends_on': ['rabbitmq']
        },
        'storage': {
            'image': 'senseyeinc/eucalyptus:storage-${TAG:-latest}',
            # 'environment': {'AWS_SHARED_CREDENTIALS_FILE': '/run/secrets/aws-credentials'},
            # 'secrets': ['aws-credentials']
        },
        'cluster_scheduler': {
            'image': 'senseyeinc/eucalyptus:compute-${TAG:-latest}',
            'ports': [f'{DASK_DASHBOARD_PORT}:8787'],
            'command': 'dask-scheduler'
        },
        'cluster_worker': {
            'image': 'senseyeinc/eucalyptus:compute-${TAG:-latest}',
            'environment': {
                'DASK_SCHEDULER_ADDRESS': 'tcp://cluster_scheduler:8786'
            },
            'volumes': ['/etc/dask:/etc/dask'],
            'command': 'python start-worker.py'
        }
    }

    # names of container to exclude
    EXCLUDE_CONTAINERS = []

    # Whether to include the dask stack i.e. scheduler + worker
    DASK_STACK = False

    # Development Tools
    MOUNTS = {}
    LOGS = ''

    @classmethod
    def setUpClass(cls):
        # Create a copy of the containers so it can be edited
        cls.containers = deep_merge(cls.CONTAINERS, {})

        # Create a Docker Stack Using the class name as an identifier
        cls.docker = DockerComposer(
            file_name=f'build/{cls.__name__}.yaml',
            project_name=cls.__name__
        )

        # Merge Dask Config
        if not cls.DASK_STACK:
            cls.EXCLUDE_CONTAINERS.extend(['cluster_worker', 'cluster_scheduler'])

        # Create Accessible Stubs form mocks and services
        cls.docker.add_services(cls.containers)

        # Set Eucalyptus Config on all containers
        for name, li in cls.MOUNTS.items():
            for point, target in dict(li).items():
                cls.docker.add_mount(name, point, target)

        # Start the compose
        cls.docker.start(
            exclude=cls.EXCLUDE_CONTAINERS,

            # Docker log configuration: env => Static Var => Container names
            logs=DOCKER_LOGS or cls.LOGS or list(cls.CONTAINERS.keys())
        )

        time.sleep(15)

    @classmethod
    def tearDownClass(cls):
        # Stop Both Stacks
        cls.docker.stop()
