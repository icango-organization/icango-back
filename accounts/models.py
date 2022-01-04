import uuid

from django.db                     import models
from django.db.models.deletion     import CASCADE
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.conf                   import settings

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError("Users must have an username")

        username = self.normalize_username(username)
        user     = self.model(username=username)
        user.set_password(password)  
        user.save(using=self._db)
            
        return user
    
    def create_superuser(self, username, password=None):
        user = self.create_user(
            username,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)

        return user

class Account(AbstractBaseUser):
    username     = models.CharField(max_length=20, unique=True)
    kakakoid     = models.CharField(max_length=20, blank=True)
    date_joined  = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)
    date_deleted = models.DateTimeField(null=True)
    is_active    = models.BooleanField(default=False)
    is_staff     = models.BooleanField(default=False)

    USERNAME_FIELD  = 'username'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        db_table = 'accounts'

class LikeStation(models.Model):
    account    = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)
    station    = models.ForeignKey('information.Station', on_delete=CASCADE)
    create_at  = models.DateTimeField(auto_now_add=True)
    update_at  = models.DateTimeField(auto_now=True, null=True)
    delete_at  = models.DateTimeField(null=True)
    is_deleted = models.BooleanField(default=0)

    class Meta:
        db_table = 'like_stations'

class Feedback(models.Model):
    account    = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE, null=True)
    uuid       = models.UUIDField(default=uuid.uuid4(), editable=False)
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
    feedback   = models.ForeignKey('Feedback', on_delete=CASCADE)
    image_path = models.CharField(max_length=300)

    class Meta:
        db_table = 'feedback_images'