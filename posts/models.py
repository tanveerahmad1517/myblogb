from django.db import models
from django.conf import settings
from mptt.managers import TreeManager
from mptt.models import MPTTModel
from django.utils.translation import pgettext_lazy
# Create your models here.
from django.contrib.auth.models import User
import misaka


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts")
    users = models.ManyToManyField(User)
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=120)
    title_html = models.TextField(editable=False)
    content = models.TextField()
    draft = models.BooleanField(default=False)
    publish = models.DateField(auto_now=False,auto_now_add=False,)
    slug = models.SlugField(unique=True)
    
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.title_html = misaka.html(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "posts:single",
            kwargs={
                "username": self.user.username,
                "pk": self.pk
            }
        )

class Profile(models.Model):
    
    first_name = models.CharField(max_length=50, db_column='first_name')
    last_name = models.CharField(max_length=50, db_column='last_name')


class UsersProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=100, default='')
    city = models.CharField(max_length=100, default='')
    website = models.URLField(default='')
    phone = models.IntegerField(default=0)
    image = models.ImageField(upload_to='profile_image', blank=True)
    def __str__(self):
        return self.user.username

