from django.db                  import models
from django.db.models.deletion  import CASCADE
from django.contrib.auth.models import AbstractUser

class Account(AbstractUser):
    # name       = models.CharField(max_length=20, blank=True)
    profile    = models.CharField(max_length=100, null=True)
    kakoid     = models.CharField(max_length=20, null=True)
    create_at  = models.DateTimeField(auto_now_add=True)
    update_at  = models.DateTimeField(auto_now=True, null=True)
    delete_at  = models.DateTimeField(null=True)
    is_deleted = models.BooleanField(default=0)

    class Meta:
        db_table = 'accounts'

class LikeStation(models.Model):
    account    = models.ForeignKey('Account', on_delete=CASCADE)
    station    = models.ForeignKey('information.Station', on_delete=CASCADE)
    create_at  = models.DateTimeField(auto_now_add=True)
    update_at  = models.DateTimeField(auto_now=True, null=True)
    delete_at  = models.DateTimeField(null=True)
    is_deleted = models.BooleanField(default=0)

    class Meta:
        db_table = 'like_stations'

class Feedback(models.Model):
    account    = models.ForeignKey('Account', on_delete=CASCADE, null=True)
    tag        = models.CharField(max_length=20, blank=True)
    title      = models.CharField(max_length=20, blank=True)
    content    = models.CharField(max_length=100, blank=True)
    create_at  = models.DateTimeField(auto_now_add=True)
    update_at  = models.DateTimeField(auto_now=True, null=True)
    delete_at  = models.DateTimeField(null=True)
    is_deleted = models.BooleanField(default=0)
    is_solved  = models.BooleanField(default=0)

    class Meta:
        db_table = 'feedbacks'

class FeedbackImage(models.Model):
    feedback = models.ForeignKey('Feedback', on_delete=CASCADE)
    img_path = models.CharField(max_length=300)

    class Meta:
        db_table = 'feedback_images'