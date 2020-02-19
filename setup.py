from setuptools import setup
from pathlib import Path

readme = str(Path(Path(__file__).parent.absolute(), 'README.md'))
long_description = open(readme, encoding='utf-8').read()

setup(
    name='eucalyptus-client',
    description='Client code for Senseye\'s Eucalyptus API.',
    author='Senseye Inc',
    version='0.1.0',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=[
        'eucalyptus_client',
        'eucalyptus_client.interceptors',
    ],
    package_dir={
        'eucalyptus_client': 'eucalyptus_client',
    },
    install_requires=[
        'grpcio',
        'eucalyptus-protos',
        'senseye_cameras==v1.0.4',
        'pyyaml',
    ],
)
