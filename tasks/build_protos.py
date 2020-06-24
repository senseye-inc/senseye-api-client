import re
import requests
from io import BytesIO
from zipfile import ZipFile
from pathlib import Path
from grpc_tools import protoc


PROTO_URL = f'http://eucalyptus-protobuf.s3-website-us-east-1.amazonaws.com'


def get_protos(version, output_path='build/protobuf'):
    """
    Fetch proto files from a remote url
    """
    # Get ZIP Binary Data from net
    complete_url = f'{PROTO_URL}/{version}.zip'
    print(f"Getting protos at {complete_url}")
    zip_data = requests.get(complete_url).content

    # Zip data must be BytesIO
    zip_data_io = BytesIO()
    zip_data_io.write(zip_data)

    # Create Zip File and extract
    ZipFile(zip_data_io).extractall(output_path)


def build_protos(input_path='build/protobuf', output_path='senseye_api_client/proto'):
    """
    Build all proto files
    """

    output_path = Path(output_path).absolute()
    input_path = Path(input_path).absolute()

    # Make output dir
    output_path.mkdir(exist_ok=True, parents=True)

    print("Building Protos...")
    print(f"Protos path: {input_path}")
    print(f"Output path: {output_path}")

    # Get proto file list
    proto_files = [str(f) for f in input_path.glob('**/*.proto')]

    # Build Protos with protoc module
    protoc.main([
        '', # Needed :(
        # Add Google's base protos
        f'-I{Path(protoc.__file__).parent / "_proto"}',
        # Add Senseye's protos
        f'-I{input_path}',
        f'--python_out={output_path}',
        f'--grpc_python_out={output_path}',
        *proto_files
    ])

    # Replace module names
    for file in output_path.glob('**/*pb2*.py'):
        with open(file, 'r') as f:
            content = re.sub(r'^(import.*_pb2)', r'from . \1', f.read(), flags=re.M)

        with open(file, 'w') as f:
            f.write(content)

        with open(output_path / 'senseye/__init__.py', 'w') as f:
            f.write('\n')

        with open(output_path / 'senseye/common/__init__.py', 'w') as f:
            f.write('\n')
