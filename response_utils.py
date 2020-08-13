from rest_framework.response import Response

"""
    This module contains class to prepare a proper server response and return it.
"""


class ApiResponse:
    """
        This is a class for constructing a common server response.

        Attributes:
            status (int): Status of api 0 or 1.
            message (int): message to be sent with response.
            data (dict): Data to be sent in api if not specified returns empty dict.
            http_status (HTTP_STATUS): This the http status sent with api if not specified explicitly restframework will
                                        handle it.
        """

    def __init__(self, status: int, message: str, data: dict = None, http_status=None, length=None,
                 count=None, total_page=None, next=None, previous=None):
        """

        :param status:  Status to be sent in response.
        :param message: message to be sent with response.
        :param data:Data to be sent in api, if not specified returns empty dict
        :param http_status: HTTP_STATUS of api, if not specified explicitly then handled by restframework
        """
        self.response = {}

        self.message = message
        self.status = status
        self.length = length
        self.http_status = http_status
        self.count = count
        self.total_page = total_page
        self.next = next
        self.previous = previous

        self.data = data if data else dict()

    def create_response(self):
        """
        Creates a Response class object and returns it.

        :py:class:: `rest_framework.response.Response`
        :return: Returns the Response of rest_framework api.
        """
        if self.count is not None:
            self.response['count'] = self.count
        if self.total_page is not None:
            self.response['total_page'] = self.total_page
        if self.next is not None:
            self.response['next'] = self.next
        if self.previous is not None:
            self.response['previous'] = self.previous
        self.response['status'] = self.status
        self.response['message'] = self.message
        if self.length:
            self.response['length'] = self.length
        self.response['data'] = self.data

        if self.http_status:
            return Response(self.response, status=self.http_status)
        else:
            return Response(self.response)


def get_error_message(serializer):
    errors = list(serializer.errors.values())
    return errors[0][0]
