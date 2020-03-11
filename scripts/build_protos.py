from io import BytesIO
import re
from zipfile import ZipFile
from pathlib import Path


PROTO_URL = f'http://eucalyptus-protobuf.s3-website-us-east-1.amazonaws.com'


def get_protos(version, output_path='build/protobuf'):
    """
    Fetch proto files from a remote url
    """
    import requests

    # Get ZIP Binary Data from net
    zip_data = requests.get(f'{PROTO_URL}/{version}.zip').content

    # Zip data must be BytesIO
    zip_data_io = BytesIO()
    zip_data_io.write(zip_data)

    # Create Zip File and extract
    ZipFile(zip_data_io).extractall(output_path)


def build_protos(input_path='build/protobuf', output_path='senseye_api_client/proto'):
    """
    Build all proto files
    """
    from grpc_tools import protoc

    output_path = Path(output_path).absolute()
    input_path = Path(input_path).absolute()

    # Make output dir
    output_path.mkdir(exist_ok=True, parents=True)

    print("Building Protos...")
    print(f"Output: {output_path}")

    # Get proto file list
    proto_files = [str(f) for f in input_path.glob('*.proto')]
    print(input_path)
    # Build Protos with protoc module
    protoc.main([
        '', # Needed :(
        f'--python_out={output_path}',
        f'--grpc_python_out={output_path}',
        f'-I{input_path}',
        *proto_files
    ])

    # Replace module names
    for file in output_path.glob('*pb2*.py'):
        with open(file, 'r') as f:
            content = re.sub(r'^(import.*_pb2)', r'from . \1', f.read(), flags=re.M)

        with open(file, 'w') as f:
            f.write(content)
