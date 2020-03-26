'''
Sends frames from a live camera to the Eucalyptus API.
Prints responses.
'''
import time
from pathlib import Path

from senseye_api_client import SenseyeApiClient


CAMERA_ID = 0
CAMERA_TYPE = 'usb'     # generic usb camera
# CAMERA_TYPE = 'ueye'    # IDS ueye camera
# CAMERA_TYPE = 'pylon'   # Basler pylon camera

start_time = time.time()
api = SenseyeApiClient(config=(Path(__file__).parent / 'config.yml'))

print(f'Start-up time: {time.time() - start_time}')

response_number = 0
start_time = time.time()

for response in api.camera_stream(CAMERA_TYPE, CAMERA_ID):
    response_number += 1
    fps = response_number / (time.time() - start_time)
    print(f"Receiving response {response_number}, overall fps: {fps}, contents: {response}")
