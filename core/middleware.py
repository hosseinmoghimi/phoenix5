
from threading import current_thread

_requests = {}

def get_request():
    t = current_thread()
    if t not in _requests:
         return None
    return _requests[t]
 


def simple_middleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        _requests[current_thread()] = request

        return response

    return middleware

 
        
# class SimpleMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#         # One-time configuration and initialization.

#     def __call__(self, request):
#         # Code to be executed for each request before
#         # the view (and later middleware) are called.

#         response = self.get_response(request)
#         self.request = request
#         _requests[current_thread()] = request

#         # Code to be executed for each request/response after
#         # the view is called.

#         return response
