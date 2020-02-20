import os
import time
from eucalyptus_client import EucalyptusApi

'''
Sends frames from a camera to the Eucalyptus API.
Prints responses.
'''

API_URL='apeye.senseye.co:27000'

# default camera id
CAMERA_ID = 0
CAMERA_TYPE = 'usb'     # generic usb camera
# CAMERA_TYPE = 'ueye'    # IDS ueye camera
# CAMERA_TYPE = 'pylon'   # Basler pylon camera

response_number = 0
start_time = time.time()

api = EucalyptusApi(url=API_URL)
for response in api.h264_stream(CAMERA_TYPE, CAMERA_ID):
    response_number += 1
    fps = response_number / (time.time() - start_time)
    print(f"Receiving Response {response_number}, overall fps: {fps}, reponse: {response}")
