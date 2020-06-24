import os
import sys
import shutil
from invoke import task
from pathlib import Path


LATEST_RELEASE = 'release/v0.4.1'

@task()
def install(c, branch=None):
    """
    Gets protos, builds protos, then installs the client.
    Protos can be specified using the --branch parameter.
    For example: `inv install --branch release/v0.3.0` will install protos from a previous version.
    """

    if branch is None:
        branch = LATEST_RELEASE

    # directory that contains setup.py
    setup_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

    # build directory
    build_path = str(Path(setup_dir, 'build'))

    # clear build directory if exists
    try:
        shutil.rmtree(build_path)
    except: pass

    # create initial build dirs
    Path(f'{build_path}/senseye').mkdir(exist_ok=True, parents=True)

    # make sure grpcio-tools is installed
    c.run(f'\
    {sys.executable} -m \
    pip install grpcio-tools'
    )

    from . build_protos import get_protos, build_protos

    # put protos into build dir
    get_protos(branch, output_path=build_path)

    # build protos
    build_protos(
        input_path=f'{build_path}',
        output_path=build_path
    )

    # install senseye-api-client
    c.run(f'\
    {sys.executable} -m \
    pip install . \
    --upgrade'
    )

    # clean up build dir
    shutil.rmtree(build_path)
