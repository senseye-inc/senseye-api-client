from . client_interceptor_generic import GenericInterceptor, ClientCallDetails

import logging
logging.basicConfig(level=0)
log = logging.getLogger(__name__)

'''
Client interceptor that modifies the header and logs a message for every message recieved
'''
class HeaderInterceptor(GenericInterceptor):
    def callback(self, item):
        print("Example client interceptor callback.")

    def intercept_service(self, continuation, client_call_details, request, request_streaming, response_streaming):
        # add metadata
        metadata = [] if client_call_details.metadata is None else list(client_call_details.metadata)
        metadata.append((
            'header',
            'value',
        ))
        client_call_details = ClientCallDetails(
            client_call_details.method, client_call_details.timeout, metadata,
            client_call_details.credentials)
        return GenericInterceptor.intercept_service(self, continuation, client_call_details, request, request_streaming, response_streaming)
