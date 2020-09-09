from django.test import TestCase

from users.models import User


class TestModels(TestCase):

    def setUp(self):
        self.User1 = User.objects.create(
            first_name="first",
            email="mail@gmail.com",
            username="username",
            phone_number="9099399929",
        )

    def create_user(self, username, first_name, email, phone_number=None):
        return User.objects.create(
            first_name=first_name,
            email=email,
            username=username,
            phone_number=phone_number,

        )

    def test_user_object(self):
        user_obj = User.objects.get(first_name="first")
        self.assertEqual(user_obj.first_name, 'first')
        self.assertEqual(user_obj.username, 'username')
        self.assertEqual(user_obj.email, 'mail@gmail.com')
        self.assertEqual(user_obj.phone_number, '9099399929')

    def test_user_qs(self):
        username1 = "TestUser1"
        username2 = "TestUser2"
        username3 = "TestUser3"
        first_name = "firstname"
        email1 = "firstname1@gmail.com"
        email2 = "firstname2@gmail.com"
        email3 = "firstname3@gmail.com"
        obj1 = self.create_user(username=username1, first_name=first_name, email=email1)
        obj2 = self.create_user(username=username2, first_name=first_name, email=email2)
        obj3 = self.create_user(username=username3, first_name=first_name, email=email3)
        qs1 = User.objects.filter(first_name=first_name)
        self.assertEqual(qs1.count(), 3)
        qs2 = User.objects.filter(first_name='first')
        self.assertEqual(qs2.count(), 1)
        qs3 = User.objects.filter(username=username1)
        self.assertEqual(qs3.count(), 1)
