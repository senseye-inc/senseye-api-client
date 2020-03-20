from setuptools import setup
from setuptools.command.build_py import build_py

from pathlib import Path
from zipfile import ZipFile
from io import BytesIO

readme = str(Path(Path(__file__).parent.absolute(), 'README.md'))
long_description = open(readme, encoding='utf-8').read()

PROTO_VERSION = 'release/v0.3.1'


class BuildPyCommand(build_py):
    """Build Hook"""

    def run(self):
        from scripts.build_protos import get_protos, build_protos

        # Fetch Proto Files
        get_protos(PROTO_VERSION, output_path='build/protobuf')

        # Build Proto Files
        build_protos(
            input_path='build/protobuf',
            output_path='senseye_api_client/proto'
        )
        build_py.run(self)


setup(
    name='senseye-api-client',
    description='Client code for Senseye\'s Eucalyptus API.',
    author='Senseye Inc',
    version='0.1.0',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=[
        'senseye_api_client',
        'senseye_api_client.interceptors',
        'senseye_api_client.proto',
    ],
    package_dir={
        'senseye_api_client': 'senseye_api_client',
    },
    install_requires=[
        'grpcio',
        'senseye-cameras==v1.0.4',
        'pyyaml',
        'pyjwt',
    ],
    project_urls={
        "Homepage": "http://senseye.co/",
        "Documentation": "https://senseye-api-client.readthedocs.io/en/latest/",
        "Source Code": "https://github.com/senseyeinc/senseye-api-client",
    },
    cmdclass={
        # Custom Build hook
        'build_py': BuildPyCommand,
    },
)
