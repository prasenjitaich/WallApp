import logging

from django.template.loader import render_to_string
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_yasg.utils import swagger_auto_schema

import constants
import utils
from response_utils import ApiResponse, get_error_message
from users.models import User
from users.serializers import UserSerializer, CustomTokenObtainPairSerializer

logger = logging.getLogger('django')


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom token class for add user info with token response.
    """
    serializer_class = CustomTokenObtainPairSerializer


class UsersList(APIView):
    """
    Class is used for list all the user or create new user.
    """
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(operation_description="Api is used to get all user detail"
                                               "from the application",
                         responses={200: UserSerializer()})
    def get(self, request):
        """
        Function is used to get all the user list.
        :param request: request header with required info.
        :return: user list
        """
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        api_response = ApiResponse(status=1, data=serializer.data, message=constants.USERS_GET_SUCCESS,
                                   http_status=status.HTTP_200_OK)
        return api_response.create_response()

    @swagger_auto_schema(request_body=UserSerializer, operation_description="API is used to post the user detail "
                                                                            "and store data inside database")
    def post(self, request):
        """
        Function is used to create new object or value in table and return status.
        :param request: request header with user info for creating new object.
        :return: user info
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            context = {
                'username': serializer.data['username'],
                'site_url': constants.SITE_URL + constants.LOGIN
            }
            # render email html
            email_html_message = render_to_string('email_templates/register_success.html', context)
            utils.send_email(subject="WELCOME!", recipient=[serializer.data['email']], body=email_html_message)
            api_response = ApiResponse(status=1, data=serializer.data, message=constants.CREATE_USER_SUCCESS,
                                       http_status=status.HTTP_201_CREATED)
            return api_response.create_response()
        api_response = ApiResponse(status=0, message=get_error_message(serializer),
                                   http_status=status.HTTP_400_BAD_REQUEST)
        return api_response.create_response()


class UserDetails(APIView):
    """
    Class is used for retrieve, update or delete a user instance.
    """
    permission_classes = [IsAuthenticated, ]

    @swagger_auto_schema(operation_description="Api is used to get particular user detail"
                                               "from the application",
                         responses={200: UserSerializer()})
    def get(self, request, pk):
        """
        Function is used for get user info with pk
        :param request: request header with required info.
        :param pk: primary key of a object.
        :return: user info or send proper error status
        """
        try:
            user = User.objects.get(id=pk)
        except User.DoesNotExist as e:
            logger.exception(e)
            api_response = ApiResponse(status=0, message=constants.USER_DOES_NOT_EXIST,
                                       http_status=status.HTTP_404_NOT_FOUND)
            return api_response.create_response()
        serializer = UserSerializer(user)
        api_response = ApiResponse(status=1, data=serializer.data, message=constants.GET_USER_SUCCESS,
                                   http_status=status.HTTP_200_OK)
        return api_response.create_response()

    @swagger_auto_schema(request_body=UserSerializer, operation_description="API is used to update the user details "
                                                                            "and store data inside database")
    def put(self, request, pk):
        """
        Function is used for modify user info
        :param request: request header with required info.
        :param pk: primary key of a object.
        :return: user info or send proper error status
        """
        try:
            user = User.objects.get(id=pk)
        except User.DoesNotExist as e:
            logger.exception(e)
            api_response = ApiResponse(status=0, message=constants.USER_DOES_NOT_EXIST,
                                       http_status=status.HTTP_404_NOT_FOUND)
            return api_response.create_response()
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            api_response = ApiResponse(status=1, data=serializer.data, message=constants.UPDATE_USER_SUCCESS,
                                       http_status=status.HTTP_201_CREATED)
            return api_response.create_response()
        api_response = ApiResponse(status=0, message=get_error_message(serializer),
                                   http_status=status.HTTP_400_BAD_REQUEST)
        return api_response.create_response()

    @swagger_auto_schema(operation_description="API is used to delete the user details "
                                               "from the database")
    def delete(self, request, pk):
        """
        Function is used for deleting user object
        :param request: request header with required info.
        :param pk: primary key of a object.
        :return: 200 ok or error message
        """
        try:
            user = User.objects.get(id=pk)
        except User.DoesNotExist as e:
            logger.exception(e)
            api_response = ApiResponse(status=0, message=constants.USER_DOES_NOT_EXIST,
                                       http_status=status.HTTP_404_NOT_FOUND)
            return api_response.create_response()
        user.delete()
        api_response = ApiResponse(status=1, message=constants.DELETE_USER_SUCCESS, http_status=status.HTTP_200_OK)
        return api_response.create_response()


class ChangePasswordView(APIView):
    """
    Class is used for change the password of the user.
    """
    permission_classes = [IsAuthenticated, ]

    @swagger_auto_schema(request_body=UserSerializer,
                         operation_description="API is used to Update the password for the user")
    def put(self, request):
        """
        Function is used for modify the password
        :param request: request header with required info.
        :return: user info or proper error message
        """
        user = request.user
        if user:
            data = {"password": request.data['password']}
            serializer = UserSerializer(user, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                api_response = ApiResponse(status=1, data=serializer.data, message=constants.CHANGE_PASSWORD_SUCCESS,
                                           http_status=status.HTTP_201_CREATED)
                return api_response.create_response()
            api_response = ApiResponse(status=0, message=get_error_message(serializer),
                                       http_status=status.HTTP_400_BAD_REQUEST)
            return api_response.create_response()
        api_response = ApiResponse(status=0, message=constants.USER_DOES_NOT_EXIST,
                                   http_status=status.HTTP_404_NOT_FOUND)
        return api_response.create_response()
