import time
from senseye_api_client import SenseyeApiClient

'''
Sends frames from a camera to the Eucalyptus API.
Prints responses.
'''

API_URL='apeye.senseye.co:27000'

VIDEO_URI = 'https://www.sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4'
response_number = 0
start_time = time.time()

api = SenseyeApiClient(url=API_URL)
for response in api.video(VIDEO_URI):
    response_number += 1
    fps = response_number / (time.time() - start_time)
    print(f"Receiving Response {response_number}, overall fps: {fps}, reponse: {response}")
