from pathlib import Path
from setuptools import setup
from setuptools.command.build_py import build_py


PROTO_VERSION = 'release/v0.3.1'

readme = str(Path(Path(__file__).parent.absolute(), 'README.md'))
long_description = open(readme, encoding='utf-8').read()

# Temporary directory to build 'senseye' package
Path('build/senseye').mkdir(exist_ok=True, parents=True)


class BuildPyCommand(build_py):
    """
    Build Hook
    """
    def run(self):
        from scripts.build_protos import get_protos, build_protos

        # Fetch Proto Files
        get_protos(PROTO_VERSION, output_path='build/protobuf')

        # Build Proto Files
        build_protos(
            input_path='build/protobuf',
            output_path='build'
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
        'senseye',
        'senseye_api_client',
        'senseye_api_client.interceptors',
    ],
    package_dir={
        'senseye': 'build/senseye',
        'senseye_api_client': 'senseye_api_client',
    },
    package_data={
        "senseye": ["**/*.py"],
    },
    install_requires=[
        'grpcio',
        'grpcio-tools',
        'senseye-cameras>=v1.0.8',
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
    }
)
