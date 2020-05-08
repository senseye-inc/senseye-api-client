import logging
import queue
import uuid

import grpc
from senseye.common.common_pb2 import VideoStreamRequest, VideoRequest
from senseye.gateway.gateway_service_pb2_grpc import GatewayStub
from senseye_cameras import Stream

from . utils import load_config
from . video_task import VideoTask


log = logging.getLogger(__name__)


class SenseyeApiClient():
    def __init__(self, config=None):
        if isinstance(config, dict):
            config = config.copy()
        else:
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

    def predict_bac(self, video_uri):
        return self._predict_feature('PredictBAC', video_uri)

    def predict_fatigue(self, video_uri):
        return self._predict_feature('PredictFatigue', video_uri)

    def predict_cogload(self, video_uri):
        return self._predict_feature('PredictCognitiveLoad', video_uri)

    def stream_cog_load(self, camera_type, camera_id):
        return self._camera_stream('PredictCognitiveLoadStream', camera_type, camera_id)

    def stream_eye_metrics(self, camera_type, camera_id):
        return self._camera_stream('GetEyeMetricsStream', camera_type, camera_id)

    def _predict_feature(self, fn_name, video_uri):
        # Get the stub Function
        if not self.channel:
            log.info("Connecting to API server")
            self.connect()

        stub_fn = getattr(self.stub, fn_name)

        metadata = self.config.get('request_metadata')
        id = stub_fn(
            VideoRequest(video_uri=video_uri, video_id=str(uuid.uuid4())),
            metadata=metadata
        ).id
        return VideoTask(self.stub, id, metadata=metadata)

    def _camera_stream(self, fn_name, camera_type, camera_id):
        # Get the Function name to call
        if not self.channel:
            log.info("Connecting to API server")
            self.connect()

        stub_fn = getattr(self.stub, fn_name)
        h264_chunks = queue.Queue(maxsize=100)
        video_id = str(uuid.uuid4())

        Stream(
            input_type=camera_type, id=camera_id,
            output_type='h264_pipe', output_config={
                'callback': lambda chunk: h264_chunks.put(chunk),
            },
            reading=True,
            writing=True,
        )

        # Create Generator Function for stream
        def gen():
            while True:
                frame = h264_chunks.get(block=True, timeout=10)
                yield VideoStreamRequest(content=frame, video_id=video_id)

        return stub_fn(
            gen(),
            metadata=self.config.get('request_metadata')
        )
