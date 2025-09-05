from rest_framework.exceptions import APIException
from rest_framework import status
from django.utils.translation import gettext_lazy as _


class BadRequestException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = {"Error": "Please Check Your Request Data, And Verify If They Are All Correct"}
    default_code = 'bad_request'

    def __init__(self, detail=None, code=None):
        super().__init__(detail, code)

class BloggyServerError(APIException):
    default_detail = _('A server error occurred.')
    default_code = 'internal_server_error'

class ServiceUnavailableException(APIException):
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    default_detail = {"Error": "The Service Is Unavailable"}
    default_code = 'service_unavailable'

class Conflict(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = {"Error": "A conflict occurred"}
    default_code = 'conflict'
