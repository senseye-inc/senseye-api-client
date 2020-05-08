import nose.tools as nt
from nose.plugins.attrib import attr
import time
from senseye_api_client import SenseyeApiClient

from . utils.integration_test import IntegrationTest
from . utils.config import DOCKER_HOSTNAME


@attr('cluster-required')
class ApiTest(IntegrationTest):

    CONFIG = {
        'server_address': f'{DOCKER_HOSTNAME}:{IntegrationTest.GRPC_PORT}',
        'secure': False
    }

    DASK_STACK = True

    DOCKER_LOGS = ['gateway', 'compute-tasks']

    def setUp(self):
        self.api = SenseyeApiClient(self.CONFIG)

    def test_static_video(self):
        task = self.api.predict_bac('http://senseye-video-footage.s3.amazonaws.com/okr_256_frames.mp4')
        nt.assert_is_not_none(task.id)

        for i in range(60):
            time.sleep(1)
            print("Waiting...")
            if task.get_status() != 'PENDING':
                break

        nt.assert_equal(task.get_status(), 'SUCCESS')
        nt.assert_equal(len(task.get_result().results), 1)
