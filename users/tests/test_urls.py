from django.test import SimpleTestCase
from django.urls import reverse, resolve
from rest_framework_simplejwt.views import TokenRefreshView,token_verify
from users.views import CustomTokenObtainPairView,UsersList,UserDetails


class TestUrls(SimpleTestCase):

    def test_token_obtain_url_is_resolved(self):
        url = reverse("token_obtain_pair")
        self.assertEquals(resolve(url).func.view_class, CustomTokenObtainPairView)

    def test_token_refresh_url_is_resolved(self):
        url = reverse("token_refresh")
        self.assertEquals(resolve(url).func.view_class, TokenRefreshView)

    def test_token_verify_url_is_resolved(self):
        url = reverse("token_verify")
        self.assertEquals(resolve(url).func, token_verify)

    def test_users_list_url_is_resolved(self):
        url = reverse("users_list")
        self.assertEquals(resolve(url).func.view_class, UsersList)

    def test_user_detail_url_is_resolved(self):
        url = reverse("user_details", kwargs={'pk': 1})
        self.assertEquals(resolve(url).func.view_class, UserDetails)
