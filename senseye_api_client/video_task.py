from senseye.common.common_pb2 import VideoTask as VideoTaskProto


class VideoTask():
    def __init__(self, stub, id, metadata=None):
        # Stub to call on for updates
        self.stub = stub

        # ID of the task
        self.id = id

        # Pointer to the GRPC representation of a task
        self.task = VideoTaskProto(id=id)

        # Metadata to send with each request
        self.metadata= metadata

    def get_task(self):
        '''Get the task Proto object'''
        return self.stub.GetVideoTask(self.task, metadata=self.metadata)

    def get_status(self):
        '''Fetch and return the Status of this task'''
        return self.get_task().status

    def get_result(self):
        '''Fetch and return the Result of this task'''
        return self.stub.GetVideoTaskResult(self.task, metadata=self.metadata)

    def cancel(self):
        '''attempt to cancel the task'''
        self.stub.CancelVideoTask(self.task, metadata=self.metadata)
