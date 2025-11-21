# from rest_framework.views import exception_handler
# from rest_framework.response import Response
# from rest_framework import status

# def custom_exception_handler(exc, context):
#     response = exception_handler(exc, context)
#     if response is not None:
#         # Wrap DRF default response into {detail: ...} or keep existing structure
#         data = {
#             "errors": response.data
#         }
#         return Response(data, status=response.status_code)
#     # For other exceptions not handled by DRF return 500
#     return Response({"errors": "Internal server error."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# doctor_service/exceptions.py
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import traceback

def custom_exception_handler(exc, context):
    # Let DRF produce its normal Response for known exceptions (ValidationError, NotFound, etc)
    response = exception_handler(exc, context)
    if response is not None:
        return Response({"errors": response.data}, status=response.status_code)

    # For unhandled exceptions, show full traceback when DEBUG=True
    if settings.DEBUG:
        tb = traceback.format_exc()
        return Response({
            "errors": str(exc),
            "traceback": tb
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Production-safe generic message otherwise
    return Response({"errors": "Internal server error."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
