import logging

from django.core.paginator import Paginator
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema

import constants
from response_utils import ApiResponse, get_error_message
from wall.models import Wall, Comment
from wall.serializers import WallSerializer, CommentSerializer
from wall.permissions import IsGetOrIsAuthenticated

logger = logging.getLogger('django')


class WallsList(APIView):
    """
    Class is used for list all the wall or create new wall by a user.
    """
    permission_classes = [IsGetOrIsAuthenticated]

    @swagger_auto_schema(operation_description="Api is used to get all wall details"
                                               "from the application",
                         responses={200: WallSerializer()})
    def get(self, request):
        """
        Function is used to get all the Wall list.
        :param request: request header with required info.
        :return: Wall list
        """
        page_number = self.request.query_params.get('page', 1)
        page_size = self.request.query_params.get('page_size', 10)
        sort_by = self.request.query_params.get('sort_by', 'created_on')
        order = self.request.query_params.get('order', 'desc')
        search = self.request.query_params.get('search', None)

        if order == 'desc':
            sort_by = '-' + sort_by

        if search:
            walls = Wall.objects.filter(title__icontains=search).order_by(sort_by)
        else:
            walls = Wall.objects.all().order_by(sort_by)

        paginator = Paginator(walls, page_size)

        count = paginator.count
        total_page = len(paginator.page_range)
        next = paginator.page(page_number).has_next()
        previous = paginator.page(page_number).has_previous()
        serializer = WallSerializer(paginator.page(page_number), many=True)
        api_response = ApiResponse(status=1, data=serializer.data, message=constants.WALLS_GET_SUCCESS,
                                   http_status=status.HTTP_200_OK, count=count, total_page=total_page, next=next,
                                   previous=previous)
        return api_response.create_response()

    @swagger_auto_schema(request_body=WallSerializer, operation_description="API is used to post the Wall detail "
                                                                            "and store data inside database")
    def post(self, request):
        """
        Function is used to create new object or value in table and return status.
        :param request: request header with user info for creating new object.
        :return: wall info
        """
        serializer = WallSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            api_response = ApiResponse(status=1, data=serializer.data, message=constants.CREATE_WALL_SUCCESS,
                                       http_status=status.HTTP_201_CREATED)
            return api_response.create_response()
        api_response = ApiResponse(status=0, message=serializer.errors,
                                   http_status=status.HTTP_400_BAD_REQUEST)
        return api_response.create_response()


class WallDetails(APIView):
    """
    Class is used for retrieve, update or delete a wall instance.
    """
    permission_classes = [IsGetOrIsAuthenticated, ]

    @swagger_auto_schema(operation_description="Api is used to get particular wall detail"
                                               "from the application",
                         responses={200: WallSerializer()})
    def get(self, request, pk):
        """
        Function is used for get wall info with pk
        :param request: request header with required info.
        :param pk: primary key of a object.
        :return: wall info or send proper error status
        """
        try:
            wall = Wall.objects.get(id=pk)
        except Wall.DoesNotExist as e:
            logger.exception(e)
            api_response = ApiResponse(status=0, message=constants.WALL_DOES_NOT_EXIST,
                                       http_status=status.HTTP_404_NOT_FOUND)
            return api_response.create_response()
        serializer = WallSerializer(wall)
        api_response = ApiResponse(status=1, data=serializer.data, message=constants.GET_WALL_SUCCESS,
                                   http_status=status.HTTP_200_OK)
        return api_response.create_response()

    @swagger_auto_schema(request_body=WallSerializer, operation_description="API is used to update the wall details "
                                                                            "and store data inside database")
    def put(self, request, pk):
        """
        Function is used for modify wall info
        :param request: request header with required info.
        :param pk: primary key of a object.
        :return: wall info or send proper error status
        """
        try:
            wall = Wall.objects.get(id=pk)
        except Wall.DoesNotExist as e:
            logger.exception(e)
            api_response = ApiResponse(status=0, message=constants.WALL_DOES_NOT_EXIST,
                                       http_status=status.HTTP_404_NOT_FOUND)
            return api_response.create_response()
        serializer = WallSerializer(wall, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            api_response = ApiResponse(status=1, data=serializer.data, message=constants.UPDATE_WALL_SUCCESS,
                                       http_status=status.HTTP_201_CREATED)
            return api_response.create_response()
        api_response = ApiResponse(status=0, message=get_error_message(serializer),
                                   http_status=status.HTTP_400_BAD_REQUEST)
        return api_response.create_response()

    @swagger_auto_schema(operation_description="API is used to delete the wall details "
                                               "from the database")
    def delete(self, request, pk):
        """
        Function is used for deleting wall object
        :param request: request header with required info.
        :param pk: primary field to delete wall info.
        :return: 200 ok or error message
        """

        try:
            wall = Wall.objects.get(id=pk)
        except Wall.DoesNotExist as e:
            logger.exception(e)
            api_response = ApiResponse(status=0, message=constants.WALL_DOES_NOT_EXIST,
                                       http_status=status.HTTP_404_NOT_FOUND)
            return api_response.create_response()
        wall.delete()
        api_response = ApiResponse(status=1, message=constants.DELETE_WALL_SUCCESS, http_status=status.HTTP_200_OK)
        return api_response.create_response()


class CommentsList(APIView):
    """
    Class is used for list all the Comments or create new Comments.
    """
    permission_classes = [IsAuthenticated, ]

    @swagger_auto_schema(request_body=WallSerializer, operation_description="API is used to post the comment detail "
                                                                            "and store data inside database")
    def post(self, request):
        """
        Function is used to create new object or value in table and return status.
        :param request: request header with user info for creating new object.
        :return: comment info
        """
        serializer = CommentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            api_response = ApiResponse(status=1, data=serializer.data, message=constants.CREATE_COMMENT_SUCCESS,
                                       http_status=status.HTTP_201_CREATED)
            return api_response.create_response()
        api_response = ApiResponse(status=0, message=get_error_message(serializer),
                                   http_status=status.HTTP_400_BAD_REQUEST)
        return api_response.create_response()


class CommentDetails(APIView):
    """
    Class is used for retrieve, update or delete a comment instance.
    """
    permission_classes = [IsAuthenticated, ]

    @swagger_auto_schema(operation_description="Api is used to get particular comment detail"
                                               "from the application",
                         responses={200: CommentSerializer()})
    def get(self, request, pk):
        """
        Function is used for get comment info with pk
        :param request: request header with required info.
        :return: comment info or send proper error status
        """
        try:
            comment = Comment.objects.get(id=pk)
        except Comment.DoesNotExist:
            api_response = ApiResponse(status=0, message=constants.COMMENT_DOES_NOT_EXIST,
                                       http_status=status.HTTP_404_NOT_FOUND)
            return api_response.create_response()
        serializer = CommentSerializer(comment)
        api_response = ApiResponse(status=1, data=serializer.data, message=constants.GET_COMMENT_SUCCESS,
                                   http_status=status.HTTP_200_OK)
        return api_response.create_response()

    @swagger_auto_schema(request_body=CommentSerializer,
                         operation_description="API is used to update the comment details "
                                               "and store data inside database")
    def put(self, request, pk):
        """
        Function is used for modify comment info
        :param request: request header with required info.
        :return: comment info or send proper error status
        """
        try:
            comment = Comment.objects.get(id=pk)
        except Wall.DoesNotExist as e:
            logger.exception(e)
            api_response = ApiResponse(status=0, message=constants.COMMENT_DOES_NOT_EXIST,
                                       http_status=status.HTTP_404_NOT_FOUND)
            return api_response.create_response()
        serializer = CommentSerializer(comment, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            api_response = ApiResponse(status=1, data=serializer.data, message=constants.UPDATE_COMMENT_SUCCESS,
                                       http_status=status.HTTP_201_CREATED)
            return api_response.create_response()
        api_response = ApiResponse(status=0, message=get_error_message(serializer),
                                   http_status=status.HTTP_400_BAD_REQUEST)
        return api_response.create_response()

    @swagger_auto_schema(operation_description="API is used to delete the comment details "
                                               "from the database")
    def delete(self, request, pk):
        """
        Function is used for deleting comment object
        :param request: request header with required info.
        :param pk: primary field to get comment info.
        :return: 200 ok or error message
        """

        try:
            comment = Comment.objects.get(id=pk)
        except comment.DoesNotExist as e:
            logger.exception(e)
            api_response = ApiResponse(status=0, message=constants.COMMENT_DOES_NOT_EXIST,
                                       http_status=status.HTTP_404_NOT_FOUND)
            return api_response.create_response()
        comment.delete()
        api_response = ApiResponse(status=1, message=constants.DELETE_COMMENT_SUCCESS, http_status=status.HTTP_200_OK)
        return api_response.create_response()
