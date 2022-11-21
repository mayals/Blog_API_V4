from django.contrib import admin
from .models import UserModel
# https://www.django-rest-framework.org/api-guide/authentication/#with-django-admin
from rest_framework.authtoken.admin import TokenAdmin

admin.site.register(UserModel)


# https://www.django-rest-framework.org/api-guide/authentication/#with-django-admin
TokenAdmin.raw_id_fields = ['user']