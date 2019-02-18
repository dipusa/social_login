from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class CustomUser(AbstractUser):
    github_user_id = models.CharField(max_length=252)
    prf_picture_url = models.CharField(max_length=252)
