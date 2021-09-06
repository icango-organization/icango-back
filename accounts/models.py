from django.db import models
from django.db                  import models
from django.conf                import settings
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion  import CASCADE
from information.models import Station

class Account(AbstractUser):
    # name       = models.CharField(max_length=20, blank=True)
    profile    = models.CharField(max_length=100, blank=True)
    create_at  = models.DateTimeField(auto_now_add=True)
    update_at  = models.DateTimeField(auto_now=True, null=True)
    delete_at  = models.DateTimeField(null=True)
    is_deleted = models.BooleanField(default=0)

    class Meta:
        db_table = 'accounts'

class FeedBack(models.Model):
    tag        = models.CharField(max_length=20, blank=True)
    title      = models.CharField(max_length=20, blank=True)
    content    = models.CharField(max_length=100, blank=True)
    create_at  = models.DateTimeField(auto_now_add=True)
    update_at  = models.DateTimeField(auto_now=True, null=True)
    delete_at  = models.DateTimeField(null=True)
    is_deleted = models.BooleanField(default=0)
    is_solved  = models.BooleanField(default=0)

    class Meta:
        db_table = 'feedback'

class LikeStation(models.Model):
    account    = models.ForeignKey('Account', on_delete=CASCADE)
    station    = models.ForeignKey('information.Station', on_delete=CASCADE)
    create_at  = models.DateTimeField(auto_now_add=True)
    update_at  = models.DateTimeField(auto_now=True, null=True)
    delete_at  = models.DateTimeField(null=True)
    is_deleted = models.BooleanField(default=0)

    class Meta:
        db_table = 'like_stations'
