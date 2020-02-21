import os
import grpc
import logging
import queue
import jwt
from senseye_cameras import Stream

from eucalyptus_protos.gateway_service_pb2_grpc import GatewayStub
from eucalyptus_protos.compute_service_pb2 import VideoStreamRequest
from . utils import video_config, load_config

log = logging.getLogger(__name__)


class SenseyeApi():
    def __init__(self, url=None, secure=False, certificate=None, store=False):
        # Load API Config
        config = load_config()

        # add the jwt token to request metadata
        try:
            key = os.environ['SENSEYE_API_JWT_KEY']
            secret = os.environ['SENSEYE_API_JWT_SECRET']
            token = jwt.encode({'iss': key}, secret, algorithm='HS256').decode("utf-8")
            config['request_metadata'] = [('authorization', f'Bearer {token}')]
        except:
            log.warning('''
            JWT token could not be generated.
            Ensure environment variables SENSEYE_API_JWT_KEY and SENSEYE_API_JWT_SECRET are set.
            You can get a token/key from http://dev.senseye.co.''')

        # add api url to the config
        if url:
            config['api_url'] = url

        self.config = config
        self.channel = None
        self.stub = None
        self.secure = secure
        self.certificate = certificate
        self.store = store

    def connect(self):
        '''
        Connect this client to the server
        '''
        if self.secure:
            if not self.certificate:
                log.error('Attempting to create a secure channel, but no certificate was provided.')

            with open(self.certificate, 'rb') as f:
                trusted_certs = f.read()

            ssl_credentials = grpc.ssl_channel_credentials(root_certificates=trusted_certs)
            self.channel = grpc.secure_channel(self.config['api_url'], ssl_credentials)
        else:
            self.channel = grpc.insecure_channel(self.config['api_url'])

        self.stub = GatewayStub(self.channel)

    def disconnect(self):
        '''
        Disconnect this client
        '''
        self.channel.close()


    def h264_stream(self, camera_type, camera_id):
        if not self.channel:
            log.info("Connecting API to server")
            self.connect()

        h264_chunks = queue.Queue(maxsize=100)

        s = Stream(
            input_type=camera_type, id=camera_id,
            output_type='h264_pipe', output_config={
                'callback': lambda chunk: h264_chunks.put(chunk),
            },
            reading=True,
            writing=True,
        )

        config = video_config((256, 256, 3), store=self.store)

        def gen():
            yield VideoStreamRequest(
                video_config=config
            )

            while True:
                frame = h264_chunks.get(block=True, timeout=10)
                yield VideoStreamRequest(content=frame)

        return self.stub.AnalyzeVideoStream(
            gen(),
            metadata=self.config['request_metadata'])
