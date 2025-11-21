from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import traceback
from django.conf import settings

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        return Response({"errors": response.data}, status=response.status_code)

    if settings.DEBUG:
        return Response({
            "errors": str(exc),
            "traceback": traceback.format_exc()
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(
        {"errors": "Internal server error."},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )
