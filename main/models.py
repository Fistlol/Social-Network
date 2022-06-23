import jwt
import datetime
from datetime import datetime
from datetime import timedelta
from django.conf import settings
from django.db import models
from django.core import validators
from django.contrib.auth.models import AbstractBaseUser

from .managers import UserManager


class User(AbstractBaseUser):
    username = models.CharField(db_index=True, max_length=255, unique=True)
    last_activity = models.DateTimeField(null=True, blank=True)
    email = models.EmailField(validators=[validators.validate_email], unique=True, blank=False)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ('username',)

    objects = UserManager()

    def __str__(self):
        return self.username

    @property
    def token(self):
        return self._generate_jwt_token()

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=60)

        token = jwt.encode({
            'id': self.pk,
            'exp': dt.utcfromtimestamp(dt.timestamp())
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_author')
    text = models.TextField(null=False, blank=True)
    created_at = models.DateTimeField("date published", auto_now_add=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ['-created_at']


class Likes(models.Model):
    user_like = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='user_like')
    liked_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='liked_post_id')
    like_datetime = models.DateTimeField(default=datetime.now, verbose_name="when it liked")

    def __str__(self):
        return self.user_like.username

    class Meta:
        ordering = ['-like_datetime']
        unique_together = ('user_like', 'liked_post')
