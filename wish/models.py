from django.db import models
from datetime import datetime
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def validator(self, data):
        errors={}
        if len(data['first_name']) < 2:
            errors['first_name'] = "First Name must be at least 2 characters"
        if len(data['last_name']) < 2:
            errors['last_name'] = "Last Name must be at least 2 characters"
        if not EMAIL_REGEX.match(data['email']):
            errors['email'] = "Email is invalid"
        if data['password'] != data['cpassword']:
            errors['password'] = "Passwords do not match"
        if len(data['password']) < 8:
            errors['lengthpassword'] = "Password must be at least 8 characters"
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.CharField(max_length=60)
    password = models.CharField(max_length=255)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    objects = UserManager()

class WishManager(models.Manager):
    def validator(self, data):
        errors={}
        if len(data['wish']) < 3:
            errors['wish'] = "Wish must be at least 3 characters"
        if len(data['desc']) < 3:
            errors['desc'] = "Description must be at least 3 characters"
        return errors


class Wish(models.Model):
    wish = models.CharField(max_length=255)
    desc = models.TextField()
    wished_by = models.ForeignKey(User, related_name='wish', on_delete=models.CASCADE)
    liked_by = models.ManyToManyField(User, related_name='liked')
    grant = models.BooleanField(default = False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    objects = WishManager()