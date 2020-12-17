from pathlib import Path
from setuptools import setup

readme = str(Path(Path(__file__).parent.absolute(), 'README.md'))
long_description = open(readme, encoding='utf-8').read()

setup(
    name='senseye-api-client',
    version='0.2.2',
    description='Senseye API Python Client',
    url='https://github.com/senseye-inc/senseye-api-client',
    author='Senseye, Inc.',
    license='BSD-3-Clause',
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
        'grpcio>=1.34.0,<2.0',
        'google-api-python-client',
        'senseye-cameras>=1.0.9',
        'pyyaml',
        'pyjwt',
    ],
    project_urls={
        "Homepage": "http://senseye.co/",
        "Documentation": "https://senseye-api-client.readthedocs.io/en/latest/",
        "Source Code": "https://github.com/senseye-inc/senseye-api-client",
    },
)
