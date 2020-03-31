'''
Sends frames from a static video to the Eucalyptus API.
Prints responses.
'''
from pathlib import Path
from time import sleep

from senseye_api_client import SenseyeApiClient


VIDEO_URI = 'http://senseye-video-footage.s3.amazonaws.com/okr_256_frames.mp4'

api = SenseyeApiClient(config=(Path(__file__).parent / 'config.yml'))
# api = SenseyeApiClient(config=(Path(__file__).parent / 'config.yml'))

video = api.video(VIDEO_URI)
print(f"Video Submitted. Id: {video.task_id}")

while video.get_status() == 'PENDING':
    print(f"Waiting for video to finish...")
    sleep(1)

print(video.get_result())
