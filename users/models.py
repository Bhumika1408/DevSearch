from django.db import models
from django.contrib.auth.models import User
import uuid
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver

# Create your models here.
class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True,related_name='user_profile')
    name=models.CharField(max_length=200,blank=True,null=True)
    email=models.EmailField(max_length=500,blank=True,null=True)
    username=models.CharField(max_length=200,null=True,blank=True)
    location=models.CharField(max_length=200,blank=True,null=True)
    short_intro=models.CharField(max_length=200,null=True,blank=True)

    bio=models.TextField(blank=True,null=True)
    profile_image=models.ImageField(null=True,blank=True,upload_to='profiles/',default="profiles/user-default_MNwPXBg.png")
    social_github=models.CharField(max_length=200,blank=True,null=True)
    social_twitter=models.CharField(max_length=200,blank=True,null=True)
    social_linkedin=models.CharField(max_length=200,blank=True,null=True)
    social_youtube=models.CharField(max_length=200,blank=True,null=True)
    social_website=models.CharField(max_length=200,blank=True,null=True)
    created=models.DateTimeField(auto_now_add=True),
    id=models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)

    def __str__(self):
        return str(self.username)
    
class Skill(models.Model):
    owner=models.ForeignKey(Profile,on_delete=models.CASCADE,null=True)
    name=models.CharField(max_length=200,null=True,blank=True)
    description=models.TextField(null=True,blank=True)
    created=models.DateTimeField(auto_now_add=True),
    id=models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)

    def __str__(self):
        return str(self.name)
    
