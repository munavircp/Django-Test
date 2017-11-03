from django.db import models
from django.contrib.auth.models import User, Permission 
from django.db.models.signals import post_save

# Create your models here.

#f = FileSystemStorage(location='/profile_image')


class UserProfile(models.Model):
    user = models.OneToOneField(User, null=True, blank=True)
    description = models.CharField(max_length=100, default='')
    city = models.CharField(max_length=100, default='')
    website = models.URLField(default='')
    phone = models.IntegerField(default=0)
    image = models.ImageField(upload_to='profile_image', blank=True, null=True)

    def __str__(self):
        return self.user.username

def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])


post_save.connect(create_profile, sender=User)
