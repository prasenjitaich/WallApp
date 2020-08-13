from django.test import TestCase, Client
from django.urls import reverse


from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework_simplejwt.views import TokenRefreshView

import constants
from users.models import User
from users.views import CustomTokenObtainPairView, UsersList, UserDetails


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.token_obtain_pair_url = reverse('token_obtain_pair')
        self.token_refresh_url = reverse('token_refresh')
        self.users_list_url = reverse('users_list')
        self.data = {"first_name": "testname",
                     "last_name": "abcs267",
                     "username": "testuser",
                     "email": "test.email@gmail.com",
                     "phone_number": "7627655653",
                     "password": "Admin@123",
                     }
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
            first_name='abc123',
            last_name='test123',
            username='Admin12',
            email="abc123@gmail.com",
            phone_number="9276233737",
            password='Admin@123',
            is_staff=True,
            is_superuser=True,
            is_active=True
        )

    def create_user(self, username, first_name, email, phone_number=None):
        return User.objects.create(
            first_name=first_name,
            email=email,
            phone_number=phone_number,
            username=username,
        )

    def test_success_user_get_data(self):
        # GET METHOD
        obj = self.create_user(username="get_user", first_name="get_name", email="get@gmail.com",
                               phone_number="7236839893")
        detail_url = reverse('user_details', kwargs={'pk': obj.id})

        request = self.factory.get(self.users_list_url)
        force_authenticate(request, user=obj)
        response1 = UsersList.as_view()(request)
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response1.data["status"], 1)
        self.assertEqual(response1.data["message"], constants.USERS_GET_SUCCESS)

        request = self.factory.get(detail_url)
        force_authenticate(request, user=obj)
        response2 = UserDetails.as_view()(request, obj.id)
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(response2.data["status"], 1)
        self.assertEqual(response2.data["message"], constants.GET_USER_SUCCESS)
        self.assertEqual(response2.data["data"]["username"], obj.username)
        self.assertEqual(response2.data["data"]["first_name"], obj.first_name)
        self.assertEqual(response2.data["data"]["email"], obj.email)
        self.assertEqual(response2.data["data"]["phone_number"], obj.phone_number)

    def test_success_user_success_post_data(self):
        request = self.factory.post(self.users_list_url, data=self.data)
        response = UsersList.as_view()(request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["status"], 1)
        self.assertEqual(response.data["message"], constants.CREATE_USER_SUCCESS)
        self.assertEqual(response.data["data"]["username"], self.data.get("username"))
        self.assertEqual(response.data["data"]["first_name"], self.data.get("first_name"))
        self.assertEqual(response.data["data"]["last_name"], self.data.get("last_name"))
        self.assertEqual(response.data["data"]["email"], self.data.get("email"))
        self.assertEqual(response.data["data"]["phone_number"], self.data.get("phone_number"))

    def test_success_user_update_data(self):
        obj = self.create_user(username="update_user", first_name="update_name", email="update@gmail.com",
                               phone_number="7236839893")
        user_details_url = reverse('user_details', kwargs={'pk': obj.id})
        request = self.factory.put(user_details_url, data=self.data)
        force_authenticate(request, user=self.user)
        response = UserDetails.as_view()(request, obj.id)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["status"], 1)
        self.assertEqual(response.data["message"], constants.UPDATE_USER_SUCCESS)
        self.assertNotEqual(response.data["data"]["username"], obj.username)
        self.assertNotEqual(response.data["data"]["first_name"], obj.first_name)
        self.assertNotEqual(response.data["data"]["email"], obj.email)
        self.assertNotEqual(response.data["data"]["phone_number"], obj.phone_number)
        self.assertEqual(response.data["data"]["username"], self.data.get("username"))
        self.assertEqual(response.data["data"]["first_name"], self.data.get("first_name"))
        self.assertEqual(response.data["data"]["last_name"], self.data.get("last_name"))
        self.assertEqual(response.data["data"]["email"], self.data.get("email"))
        self.assertEqual(response.data["data"]["phone_number"], self.data.get("phone_number"))

    def test_success_user_delete_data(self):
        obj = self.create_user(username="del_user", first_name="del_name", email="del@gmail.com",
                               phone_number="7236839893")
        delete_url = reverse('user_details', kwargs={'pk': obj.id})
        request = self.factory.delete(delete_url)
        force_authenticate(request, user=obj)
        response = UserDetails.as_view()(request, obj.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["status"], 1)
        self.assertEqual(response.data["message"], constants.DELETE_USER_SUCCESS)
        user = User.objects.filter(id=obj.id).first()
        self.assertEqual(user, None)

    def test_success_get_token_pair_data(self):
        request = self.factory.post(self.token_obtain_pair_url, data=
        {
            "username": self.user.username,
            "password": "Admin@123"
        },
                                    )

        response = CustomTokenObtainPairView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['refresh'])
        self.assertTrue(response.data['access'])

    def test_fail_get_token_pair_data(self):
        request = self.factory.post(self.token_obtain_pair_url, data=
        {
            "username": self.user.username,
            "password": "Incorrect@123"
        },
                                    )
        response = CustomTokenObtainPairView.as_view()(request)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data["detail"], "No active account found with the given credentials")

    def test_success_get_api_token_refresh_data(self):
        request = self.factory.post(self.token_obtain_pair_url, data=
        {
            "username": self.user.username,
            "password": "Admin@123"
        },
                                    )
        response1 = CustomTokenObtainPairView.as_view()(request)
        request = self.factory.post(self.token_refresh_url, data=
        {
            "refresh": response1.data["refresh"]
        }

                                    )
        response2 = TokenRefreshView.as_view()(request)
        self.assertEqual(response2.status_code, 200)

    def test_fail_get_api_token_refresh_data(self):
        request = self.factory.post(self.token_obtain_pair_url, data=
        {
            "username": self.user.username,
            "password": "Admin@123"
        },
                                    )
        response1 = CustomTokenObtainPairView.as_view()(request)
        request = self.factory.post(self.token_refresh_url, data=
        {
            "refresh": response1.data["refresh"] + "wrong"
        }

                                    )
        response2 = TokenRefreshView.as_view()(request)
        self.assertEqual(response2.status_code, 401)
        self.assertEqual(response2.data["code"], "token_not_valid")
        self.assertEqual(response2.data["detail"], "Token is invalid or expired")
