from django.test import SimpleTestCase
from django.urls import reverse, resolve
from wall.views import WallsList, WallDetails, CommentsList, CommentDetails


class TestUrls(SimpleTestCase):

    def test_walls_list_url_is_resolved(self):
        url = reverse("walls_list")
        self.assertEquals(resolve(url).func.view_class, WallsList)

    def test_wall_detail_url_is_resolved(self):
        url = reverse("wall_details", kwargs={'pk': 1})
        self.assertEquals(resolve(url).func.view_class, WallDetails)

    def test_comment_list_url_is_resolved(self):
        url = reverse("comments_list")
        self.assertEquals(resolve(url).func.view_class, CommentsList)

    def test_comment_detail_url_is_resolved(self):
        url = reverse("comment_details", kwargs={'pk': 1})
        self.assertEquals(resolve(url).func.view_class, CommentDetails)
