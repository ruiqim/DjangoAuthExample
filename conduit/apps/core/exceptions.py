from rest_framework.views import exception_handler

def core_exception_handler(exc, context):
    # Handle exceptions by delegating to default exception handler by DRF
    # In the case of an exception to be handled, the DRF response should still
    # be generated and access upfront
    response = exception_handler(exc, context)
    handlers = {
        'ValidationError':_handle_generic_error
    }

    # Check to identify the current exception. This is where conditional logic
    # will dictate whether a custom exception is deployed or let Django
    # REST framework handle it.

    exception_class = exc.__class__.__name__

    if exception_class in handlers:
        # If the exception is accounted for, the custome return will provide
        # a response, otherwise return the initial response
        return handlers[exception_class](exc, context, response)

    return response


def _handle_generic_error(exc, context, response):
    # The most simple exception handler to be created
    # Take DRF response and wrap it with `errors` key so Django can handle

    response.data = {
        'errors': response.data
    }

    return response
