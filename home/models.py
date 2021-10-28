from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.dispatch import receiver


class Feedback(models.Model):
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    email = models.CharField(max_length=120)
    phone = models.CharField(max_length=12)
    remark = models.TextField()
    date = models.DateField()

    def __str__(self):
        return self.firstname

