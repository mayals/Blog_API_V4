from django.db import models
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import MinLengthValidator
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone
from django.contrib.auth.base_user import BaseUserManager
from django.core.mail import send_mail
# https://github.com/django/django/blob/main/django/contrib/auth/models.py

# https://www.django-rest-framework.org/api-guide/authentication/#generating-tokens
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from blogApp.models import Post

from .user_manager import UserModelManger
import uuid

# https://github.com/django/django/blob/main/django/contrib/auth/models.py#L136


# https://github.com/django/django/blob/main/django/contrib/auth/models.py#L334

#----------------------------------------[  UserModel  ]----------------------------------------------------#

class UserModel(AbstractBaseUser, PermissionsMixin):
    """
    Users within the Django authentication system are represented by this model.
    Username , password and email are required. Other fields are optional.
    """

    
    M = 'Male'
    F = 'Female'
    GENDER_CHOICES=[
                    (M,'Male'),
                    (F,'Female'),
    ] 
    username_validator = UnicodeUsernameValidator()


 
    id              = models.UUIDField(primary_key=True, editable=False,default=uuid.uuid4)
    username        = models.CharField(  
                                max_length=50,
                                null = True,
                                unique=True,
                                editable = False,
                                help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                                validators=[username_validator],   
                                error_messages={"unique": "A user with that username already exists.",},      
    )
    email           = models.EmailField(
                                null = True,
                                unique=True,
                                editable = True
    )
    first_name      = models.CharField(max_length=50, null=True, blank=True)
    last_name       = models.CharField(max_length=50, null=True, blank=True)
    favorites       = models.ManyToManyField(Post, related_name='users_favos', null=True, blank=True)
    is_staff        = models.BooleanField(
                                default=False,
                                help_text="Designates whether the user can log into this admin site.",
    )
    is_active       = models.BooleanField(
                                default=True,
                                help_text="Designates whether this user should be treated as active.Unselect this instead of deleting accounts."         
    )
    date_joined     = models.DateTimeField(default=timezone.now)
    password        = models.CharField( max_length=16,
                                        validators=[MinLengthValidator(8)],
                                        # editable = False,
                                        null=True
                                        
    )
    # Last login    this field --> come as default from AbstractBaseUser
    
    # ------------------------------- my extra fields --- you can add more fields ------------------------------------------
    # add more fields:
    # we can now add any extra_fields to this UserModel because we customize user model using inherit from AbstractBaseUser 
    gender          = models.CharField(choices=GENDER_CHOICES, default='F', max_length=6)
    born_date       = models.DateTimeField(null = True)  
    country         = models.CharField(max_length=30, blank=True, null = True)
    avatar          = models.ImageField(upload_to = "avatars/%Y/%m/%d/", blank=True, null=True)
    bio             = models.TextField(max_length=500, null=True, blank=True)
    website         = models.URLField(max_length=200, null=True, blank=True)
    

    objects = UserModelManger()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    class Meta:
            ordering = ('-date_joined',)
            verbose_name = 'UserModel'
            verbose_name_plural = 'UsersModel'

    
           

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)


    # https://www.django-rest-framework.org/api-guide/authentication/#generating-tokens
    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_auth_token(sender, instance=None, created=False, **kwargs):
        if created:
            Token.objects.create(user=instance)


