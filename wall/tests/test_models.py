from django.test import TestCase

from wall.models import Wall, Comment


class TestModels(TestCase):

    def setUp(self):
        self.wall1 = Wall.objects.create(
            title="test_title",
            content="test_content",
        )
        self.comment1 = Comment.objects.create(
            comment_content="test_comment",
            wall=self.wall1,
        )

    def create_wall(self, title, content):
        return Wall.objects.create(
            title=title,
            content=content,
        )

    def create_comment(self, content, wall):
        return Comment.objects.create(
            comment_content=content,
            wall=wall,
        )

    def test_wall_object(self):
        wall_obj = Wall.objects.get(title="test_title")
        self.assertEqual(wall_obj.title, 'test_title')
        self.assertEqual(wall_obj.content, 'test_content')

    def test_comment_object(self):
        comment_obj = Comment.objects.get(id=self.comment1.id)
        self.assertEqual(comment_obj.comment_content, 'test_comment')
        self.assertEqual(comment_obj.wall.id, self.wall1.id)

    def test_wall_qs(self):
        title1 = "TestTitle1"
        title2 = "TestTitle2"
        title3 = "TestTitle3"
        content1 = "Content1"
        content2 = "Content2"
        content3 = "Content3"
        obj1 = self.create_wall(title=title1, content=content1)
        obj2 = self.create_wall(title=title2, content=content2)
        obj3 = self.create_wall(title=title3, content=content3)
        qs1 = Wall.objects.filter(title='test_title')
        self.assertEqual(qs1.count(), 1)
        qs2 = Wall.objects.filter(title=title1)
        self.assertEqual(qs2.count(), 1)
        qs3 = Wall.objects.filter(title=title2)
        self.assertEqual(qs3.count(), 1)
        qs4 = Wall.objects.filter(title=title3)
        self.assertEqual(qs4.count(), 1)
        qs5 = Wall.objects.all()
        self.assertEqual(qs5.count(), 4)

    def test_comment_qs(self):
        comment_content1 = "TestContent1"
        comment_content2 = "TestContent2"
        obj1 = self.create_comment(content=comment_content1, wall=self.wall1)
        obj2 = self.create_comment(content=comment_content2, wall=self.wall1)
        qs1 = Comment.objects.all()
        self.assertEqual(qs1.count(), 3)  # Including wall1
