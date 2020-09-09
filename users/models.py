from django.db import models
from django.contrib.auth.models import AbstractUser


class BaseModel(models.Model):
    """
    This is base model which we are using for common attributes not
    included in Database as a table
    :param models.Model: Class to create a new instance of a model,
     instantiate it like any other Python class
    """
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser, BaseModel):
    """
    User class is define for the keep the user details and other information.
    :param AbstractUser: Built in class for the user in django.
    :param BaseModel: Base class which has common attribute for the
    application.
    """
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(max_length=50, blank=False, unique=True)
    phone_number = models.CharField(max_length=14, blank=True, null=True)

    def __str__(self):
        """Default object return value, it will return username
        :return self.username: Username of the user object.
        """
        return self.username
