from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser

# Create your models here.


class User(AbstractBaseUser):
    username = models.CharField(max_length=50, unique=True, null=False)
    password = models.CharField(max_length=50, null=False)


class Project(models.Model):
    name = models.CharField(unique=True, max_length=200, null=False)
    description = models.CharField(max_length=200, null=False)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Action(models.Model):
    project_id = models.ForeignKey(Project,
                                   related_name='action',
                                   on_delete=models.CASCADE,
                                   null=False)
    description = models.CharField(max_length=200, null=False)
    note = models.TextField(max_length=400, null=False)
