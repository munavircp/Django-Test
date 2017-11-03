from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone
from django.utils.text import slugify


class Post(models.Model):
    post = models.CharField(max_length=500)
    user = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Friend(models.Model):
    users = models.ManyToManyField(User)
    current_user = models.ForeignKey(User, related_name='owner', null=True)

    @classmethod
    def make_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users.add(new_friend)

    @classmethod
    def lose_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users.remove(new_friend)

# Create your models here.
# MVC MODEL VIEW CONTROLLER


#Post.objects.all().published()
#Post.objects.create(user=user, title="Some time")

#class PostQuerySet(models.query.QuerySet):
#    def not_draft(self):
#        return self.filter(draft=False)
#    
#    def published(self):
#        return self.filter(publish__lte=timezone.now()).not_draft()
#
#class PostManager(models.Manager):
#    def get_queryset(self, *args, **kwargs):
#        return PostQuerySet(self.model, using=self._db)
#            
#    def active(self, *args, **kwargs):
#        # Post.objects.all() = super(PostManager, self).all()
#        return self.get_queryset().published()
#
#
#def upload_location(post, filename):
#    #filebase, extension = filename.split(".")
#    #return "%s/%s.%s" %(instance.id, instance.id, extension)
#    PostModel = post.__class__
#    new_id = PostModel.objects.order_by("id").last().id + 1
#   
#    return "%s/%s" %(new_id, filename)
#
#class Post(models.Model):
#    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
#    title = models.CharField(max_length=120)
#    slug = models.SlugField(unique=True)
#    image = models.ImageField(upload_to=upload_location, 
#            null=True, 
#            blank=True, 
#            width_field="width_field", 
#            height_field="height_field")
#    height_field = models.IntegerField(default=0)
#    width_field = models.IntegerField(default=0)
#    content = models.TextField()
#    draft = models.BooleanField(default=False)
#    publish = models.DateField(auto_now=False, auto_now_add=False)
#    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
#    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
#
#    objects = PostManager()
#
#    def __unicode__(self):
#        return self.title
#
#    def __str__(self):
#        return self.title
#
#    def get_absolute_url(self):
#        return reverse("posts:detail", kwargs={"slug": self.slug})
#
#    class Meta:
#        ordering = ["-timestamp", "-updated"]
#       
##    @property
##    def title(self):
##        return "Title"
#
#
#
#def create_slug(post, new_slug=None):
#    slug = slugify(post.title)
#    if new_slug is not None:
#        slug = new_slug
#    qs = Post.objects.filter(slug=slug).order_by("-id")
#    exists = qs.exists()
#    if exists:
#        new_slug = "%s-%s" %(slug, qs.first().id)
#        return create_slug(post, new_slug=new_slug)
#    return slug
#
#
##from .utils import unique_slug_generator
#
#def pre_save_post_receiver(sender, post, *args, **kwargs):
#    if not post.slug:
#        instance.slug = create_slug(instance)
#        
#
#
#
#pre_save.connect(pre_save_post_receiver, sender=Post)










