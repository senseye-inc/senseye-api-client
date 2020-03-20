import time
from senseye_api_client import SenseyeApiClient

'''
Sends frames from a camera to the Eucalyptus API.
Prints responses.
'''

API_URL='apeye.senseye.co:27000'

VIDEO_URI = 'http://senseye-video-footage.s3.amazonaws.com/okr_256_frames.mp4'
response_number = 0
start_time = time.time()

api = SenseyeApiClient(url=API_URL)
for response in api.video(VIDEO_URI):
    print(f"Receiving response: {response}")
