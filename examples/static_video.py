'''
Sends frames from a static video to the Eucalyptus API.
Prints responses.
'''
from pathlib import Path

from senseye_api_client import SenseyeApiClient


VIDEO_URI = 'http://senseye-video-footage.s3.amazonaws.com/okr_256_frames.mp4'

api = SenseyeApiClient(config=(Path(__file__).parent / 'config.yml'))

for response in api.video(VIDEO_URI):
    print(f"Receiving response: {response}")
