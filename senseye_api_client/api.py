import logging
import queue

import grpc
from senseye.common.common_pb2 import VideoStreamRequest, VideoStaticRequest
from senseye.gateway.gateway_service_pb2_grpc import GatewayStub
from senseye_cameras import Stream

from . utils import video_config, load_config
from . video_task import VideoTask


log = logging.getLogger(__name__)


class SenseyeApiClient():
    def __init__(self, config=None):
        # Load API and Client config
        config = load_config(config)

        self.config = config
        self.channel = None
        self.stub = None

    def connect(self):
        '''
        Connect this client to the API server
        '''
        secure = self.config.get('secure')

        if secure and secure.get('enabled') == True:
            if not secure.get('cert_file'):
                log.error('Attempting to create a secure channel, but no certificate was provided.')
                exit()

            with open(secure.get('cert_file'), 'rb') as f:
                trusted_certs = f.read()

            ssl_credentials = grpc.ssl_channel_credentials(root_certificates=trusted_certs)
            self.channel = grpc.secure_channel(self.config['server_address'], ssl_credentials)
        else:
            self.channel = grpc.insecure_channel(self.config['server_address'])

        self.stub = GatewayStub(self.channel)

    def disconnect(self):
        '''
        Disconnect this client
        '''
        self.channel.close()

    def video(self, video_uri):
        if not self.channel:
            log.info("Connecting to API server")
            self.connect()

        request_metadata = self.config.get('request_metadata')

        id = self.stub.AnalyzeVideo(
            VideoStaticRequest(
                cv_models=[1],
                insight_models=[1],
                orm_experiments=[1],
                video_uri=video_uri,
            ),
            metadata=request_metadata
        ).result

        return VideoTask(self.stub, id, metadata=request_metadata)

    def camera_stream(self, camera_type, camera_id):
        if not self.channel:
            log.info("Connecting to API server")
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

        config = video_config((256, 256, 3), store=self.config.get('store_video', False))

        def gen():
            yield VideoStreamRequest(
                video_config=config
            )

            while True:
                frame = h264_chunks.get(block=True, timeout=10)
                yield VideoStreamRequest(content=frame)

        return self.stub.AnalyzeVideoStream(
            gen(),
            metadata=self.config.get('request_metadata'))
