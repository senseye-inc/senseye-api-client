from pathlib import Path
from setuptools import setup

readme = str(Path(Path(__file__).parent.absolute(), 'README.md'))
long_description = open(readme, encoding='utf-8').read()

setup(
    name='senseye-api-client',
    description='Client code for Senseye\'s Eucalyptus API.',
    author='Senseye Inc',
    version='0.2.2',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=[
        'senseye',
        'senseye.common',
        'senseye_api_client',
        'senseye_api_client.interceptors',
    ],
    package_dir={
        'senseye': 'build/senseye',
        'senseye.common': 'build/senseye/common',
        'senseye_api_client': 'senseye_api_client',
    },
    package_data={
        "senseye": ["**/*.py"],
    },
    install_requires=[
        'grpcio',
        'grpcio-tools',
        'google-api-python-client',
        'senseye-cameras>=v1.0.8',
        'pyyaml',
        'pyjwt',
        'requests',
        'invoke',
    ],
    project_urls={
        "Homepage": "http://senseye.co/",
        "Documentation": "https://senseye-api-client.readthedocs.io/en/latest/",
        "Source Code": "https://github.com/senseyeinc/senseye-api-client",
    },
)
