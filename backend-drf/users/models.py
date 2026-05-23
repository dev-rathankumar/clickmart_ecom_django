from django.db import models
from django.contrib.auth.models import AbstractUser


# AbstractUser = add/modify any fields.
# AbstractBaseUser = we use this if you want to get the full control over your user model
# BaseUserManager = Employee.objects = Manager  => he is the one who carries out all the actions on the model.


class User(AbstractUser):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email