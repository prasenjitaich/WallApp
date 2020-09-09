from django.test import TestCase, Client
from django.urls import reverse

from rest_framework.test import APIRequestFactory, force_authenticate

import constants
from wall.views import WallsList, WallDetails, CommentsList, CommentDetails
from users.models import User
from wall.models import Wall, Comment


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.walls_list_url = reverse('walls_list')
        self.comment_list_url = reverse('comments_list')
        self.data = {"title": "test_wall",
                     "content": "test_content",
                     }
        self.comment_data = {
            "comment_content": "test_comment",
        }
        self.factory = APIRequestFactory()
        self.wall = Wall.objects.create(
            title='title',
            content='content',
        )

    def create_user(self, username, first_name, email):
        return User.objects.create(
            first_name=first_name,
            email=email,
            username=username,
        )

    def create_wall(self, title, content, created_by=None, modified_by=None):
        return Wall.objects.create(
            title=title,
            content=content,
            created_by=created_by,
            modified_by=modified_by,
        )

    def create_comment(self, comment, wall, created_by=None, modified_by=None):
        return Comment.objects.create(
            comment_content=comment,
            wall=wall,
            created_by=created_by,
            modified_by=modified_by,
        )

    def test_success_wall_get_data(self):
        # GET METHOD
        user = self.create_user(username="test_user", first_name="test_name", email="test@gmail.com")
        obj = self.create_wall(title="get_title", content="get_content", created_by=user, modified_by=user)
        request = self.factory.get(self.walls_list_url)
        response1 = WallsList.as_view()(request)
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response1.data["status"], 1)
        self.assertEqual(response1.data["message"], constants.WALLS_GET_SUCCESS)

        detail_url = reverse('wall_details', kwargs={'pk': obj.id})
        request = self.factory.get(detail_url)
        response2 = WallDetails.as_view()(request, obj.id)
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(response2.data["status"], 1)
        self.assertEqual(response2.data["message"], constants.GET_WALL_SUCCESS)
        self.assertEqual(response2.data["data"]["title"], obj.title)
        self.assertEqual(response2.data["data"]["content"], obj.content)

    def test_success_wall_success_post_data(self):
        user = self.create_user(username="test_user", first_name="test_name", email="test@gmail.com")
        request = self.factory.post(self.walls_list_url, data=self.data)
        force_authenticate(request, user=user)
        response = WallsList.as_view()(request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["status"], 1)
        self.assertEqual(response.data["message"], constants.CREATE_WALL_SUCCESS)
        self.assertEqual(response.data["data"]["title"], self.data.get("title"))
        self.assertEqual(response.data["data"]["content"], self.data.get("content"))

    def test_success_wall_update_data(self):
        user = self.create_user(username="test_user", first_name="test_name", email="test@gmail.com")
        obj = self.create_wall(title="update_wall", content="update_content", created_by=user, modified_by=user)
        wall_details_url = reverse('wall_details', kwargs={'pk': obj.id})
        request = self.factory.put(wall_details_url, data=self.data)
        force_authenticate(request, user=user)
        response = WallDetails.as_view()(request, obj.id)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["status"], 1)
        self.assertEqual(response.data["message"], constants.UPDATE_WALL_SUCCESS)
        self.assertNotEqual(response.data["data"]["title"], obj.title)
        self.assertNotEqual(response.data["data"]["content"], obj.content)
        self.assertEqual(response.data["data"]["title"], self.data.get("title"))
        self.assertEqual(response.data["data"]["content"], self.data.get("content"))

    def test_success_wall_delete_data(self):
        user = self.create_user(username="test_user", first_name="test_name", email="test@gmail.com")
        obj = self.create_wall(title="del_wall", content="del_content")
        delete_url = reverse('wall_details', kwargs={'pk': obj.id})
        request = self.factory.delete(delete_url)
        force_authenticate(request, user=user)
        response = WallDetails.as_view()(request, obj.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["status"], 1)
        self.assertEqual(response.data["message"], constants.DELETE_WALL_SUCCESS)
        wall = Wall.objects.filter(id=obj.id).first()
        self.assertEqual(wall, None)

    def test_success_comment_success_post_data(self):
        user = self.create_user(username="test_user", first_name="test_name", email="test@gmail.com")
        request = self.factory.post(self.comment_list_url, data=self.comment_data)
        force_authenticate(request, user=user)
        response = CommentsList.as_view()(request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["status"], 1)
        self.assertEqual(response.data["message"], constants.CREATE_COMMENT_SUCCESS)
        self.assertEqual(response.data["data"]["comment_content"], self.comment_data.get("comment_content"))

    def test_success_comment_update_data(self):
        user = self.create_user(username="test_user", first_name="test_name", email="test@gmail.com")
        obj = self.create_comment(comment="update_comment", wall=self.wall, created_by=user, modified_by=user)
        details_url = reverse('comment_details', kwargs={'pk': obj.id})
        request = self.factory.put(details_url, data=self.comment_data)
        force_authenticate(request, user=user)
        response = CommentDetails.as_view()(request, obj.id)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["status"], 1)
        self.assertEqual(response.data["message"], constants.UPDATE_COMMENT_SUCCESS)
        self.assertNotEqual(response.data["data"]["comment_content"], obj.comment_content)
        self.assertEqual(response.data["data"]["comment_content"], self.comment_data.get("comment_content"))

    def test_success_comment_delete_data(self):
        user = self.create_user(username="test_user", first_name="test_name", email="test@gmail.com")
        obj = self.create_comment(comment="delete_comment", wall=self.wall, created_by=user, modified_by=user)
        delete_url = reverse('comment_details', kwargs={'pk': obj.id})
        request = self.factory.delete(delete_url)
        force_authenticate(request, user=user)
        response = CommentDetails.as_view()(request, obj.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["status"], 1)
        self.assertEqual(response.data["message"], constants.DELETE_COMMENT_SUCCESS)
        comment = Comment.objects.filter(id=obj.id).first()
        self.assertEqual(comment, None)
