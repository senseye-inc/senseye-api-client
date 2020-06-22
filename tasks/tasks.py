import os
import sys
import shutil
from invoke import task
from pathlib import Path


PROTO_VERSION = 'v0.4.1'

@task()
def install(c):
    """
    Build protos
    Install
    """
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
    get_protos(f'release/{PROTO_VERSION}', output_path=build_path)

    # build protos
    build_protos(
        input_path=f'{build_path}/protobuf',
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
