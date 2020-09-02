from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save


class CustomUser(AbstractUser):

    pass

    def __str__(self):
        return self.username



class Profile(models.Model):
    rating = models.IntegerField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="userprofile"
    )


    def save_profile(sender, instance, **kwargs):
        instance.profile.save()
    post_save.connect(save_post, sender=CustomUser)

# class Post(models.Model):
    
#     def save_post(sender, instance, **kwargs):
#         print("something")
#     post_save.connect(save_post, sender=Post)
# sender is jsut the model thats signally this to take place
# we want a signal to take place when the save method is exectued
# on post model then the sender would be the post
# so we pass i nthe senders te first argument

# link receiver 

    # user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    # user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    # related_name="profile"
# Got AttributeError when attempting to get a value for field `profile` on serializer `CustomUserSerializer`.
# The serializer field might be named incorrectly and not match any attribute or key on the `CustomUser` instance.
# Original exception text was: 'CustomUser' object has no attribute 'profile'.