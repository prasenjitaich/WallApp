from django.db import models
from users.models import User, BaseModel


class CommonModel(models.Model):
    """This is common model which we are using for common attributes not
    included in Database as a table
    :param models.Model: Class to create a new instance of a model,
     instantiate it like any other Python class
    """
    created_by = models.ForeignKey(User, null=True, related_name='%(class)s_requests_created',
                                   on_delete=models.CASCADE)
    modified_by = models.ForeignKey(User, null=True, related_name='%(class)s_requests_modified',
                                    on_delete=models.CASCADE)

    class Meta:
        abstract = True


# Create your models here.
class Wall(BaseModel, CommonModel):
    """
    Wall class is define for the keep the Wall details and other information.
    :param CommonModel:CommonModel which has common attribute for the
    application.
    :param BaseModel: Base class which has common attribute for the
    application.
    """
    title = models.CharField(max_length=50, unique=True)
    content = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_on']


class Comment(BaseModel, CommonModel):
    """
    Comment class is define for the keep the Comment details and other information.
    :param CommonModel:CommonModel which has common attribute for the
    application.
    :param BaseModel: Base class which has common attribute for the
    application.
    """
    wall = models.ForeignKey(Wall, on_delete=models.CASCADE, blank=True, null=True, related_name="comments")
    comment_content = models.CharField(max_length=200)

    def __str__(self):
        return self.comment_content

    class Meta:
        ordering = ['-created_on']
