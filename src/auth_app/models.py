from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    project = models.CharField(max_length=100, default='wtc')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

class Project(models.Model):
    id = models.AutoField(primary_key=True)
    project_name = models.CharField(max_length=255)