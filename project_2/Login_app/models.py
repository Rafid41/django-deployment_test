from django.db import models
#import the built in user model
from django.contrib.auth.models import User


# we'll use username, password and email


# if we want to add extra info to user, we'll have define a new class
class UserInfo(models.Model):
    # means user er ekta field,  UserInfo er elta field er sathe connect thakbe
    # one to one relation
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    facebook_id = models.URLField(blank = True)

    # pic upload hbe 'profile_pics' directory te
    profile_pic = models.ImageField(upload_to = 'profile_pics', blank = True)

    def __str__(self):
        return self.user.username