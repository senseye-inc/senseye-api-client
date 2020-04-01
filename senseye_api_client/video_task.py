from senseye.gateway.gateway_service_pb2 import VideoTaskRequest, VideoTaskResponse
# from senseye.common.common_pb2 import VideoStreamResponse


class VideoTask():
    def __init__(self, stub, task_id, metadata=None):
        self.stub = stub
        self.task_id = task_id
        self.metadata = metadata

    def get_task_id(self):
        return self.task_id

    def get_status(self):
        return self.stub.CheckVideoStatus(VideoTaskRequest(id=self.task_id), metadata=self.metadata).result

    def get_result(self):
        return self.stub.GetVideoResult(VideoTaskRequest(id=self.task_id), metadata=self.metadata)

    def cancel(self):
        return self.stub.CancelVideoTask(VideoTaskRequest(id=self.task_id), metadata=self.metadata).result
