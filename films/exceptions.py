from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    """
    Custom exception handler for consistent error responses
    """
    response = exception_handler(exc, context)
    
    if response is not None:
        custom_response = {
            'error': True,
            'message': str(exc),
            'status_code': response.status_code
        }
        
        if hasattr(response, 'data') and isinstance(response.data, dict):
            if 'detail' in response.data:
                custom_response['detail'] = response.data['detail']
            else:
                custom_response['detail'] = response.data
        
        response.data = custom_response
    else:
        custom_response = {
            'error': True,
            'message': 'An unexpected error occurred',
            'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR
        }
        response = Response(custom_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return response