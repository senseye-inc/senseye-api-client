import collections
import grpc

'''
Data structure that describes an RPC to be invoked.
https://grpc.github.io/grpc/python/grpc.html#grpc.ClientCallDetails
'''
class ClientCallDetails(
        collections.namedtuple(
            '_ClientCallDetails',
            ('method', 'timeout', 'metadata', 'credentials')),
        grpc.ClientCallDetails):
    pass


'''
Implementation of a generic client interceptor based on:
https://github.com/grpc/grpc/blob/master/examples/python/interceptors/headers/generic_client_interceptor.py
'''
class GenericInterceptor(
    grpc.UnaryUnaryClientInterceptor, grpc.UnaryStreamClientInterceptor,
    grpc.StreamUnaryClientInterceptor, grpc.StreamStreamClientInterceptor,
):
    def callback(self, item):
        '''
        Function to be overridden. Has access to every item before the RPC call.
        '''
        pass

    def intercept_service(self, continuation, client_call_details, request, request_streaming, response_streaming):
        '''
        Function to be overriden that has access to the client_call_details for each item passed to the intercepted channel.
        client_call_details can be overridden to modify metadata/credentials

        Args:
            client_call_details (ClientCallDetails) : object describing RPC to be invoked, including metadata that includes header information
            request_iterator: generator that contains the items in this request
            request_streaming (bool): whether the request is a stream
            response_streaming (bool): whether the response is a stream

        Returns:
            3-element tuple containing:
                client_call_details: object describing RPC to be invoked, including metadata that includes header information
                request_iterator: generator containing this streams' items
            results (list): List of GRPC EyeFeatureResult objects
        '''
        def wrapper(generator):
            while True:
                try:
                    item = next(generator)
                    self.callback(item)
                    yield item
                except StopIteration:
                    break

        new_request = wrapper(request if request_streaming else iter((request,)))

        response = continuation(
            client_call_details,
            new_request if request_streaming else next(new_request),
        )

        return response

    def intercept_unary_unary(self, continuation, client_call_details, request):
        '''Overriden class method for unary/unary RPCs'''
        return self.intercept_service(continuation, client_call_details, request, False, False)

    def intercept_unary_stream(self, continuation, client_call_details, request):
        '''Overriden class method for unary/stream RPCs'''
        return self.intercept_service(continuation, client_call_details, request, False, True)

    def intercept_stream_unary(self, continuation, client_call_details, request):
        '''Overriden class method for stream/unary RPCs'''
        return self.intercept_service(continuation, client_call_details, request, True, False)

    def intercept_stream_stream(self, continuation, client_call_details, request):
        '''Overriden class method for stream/stream RPCs'''
        return self.intercept_service(continuation, client_call_details, request, True, True)
