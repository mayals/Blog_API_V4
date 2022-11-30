from django.contrib import admin
from django.urls import path,include
from blogApp import views
from rest_framework.routers import DefaultRouter



router = DefaultRouter()

app_name = 'blogApp'

router.register('category',views.Categoryviewset,basename="category")
router.register('post',views.Postviewset,basename="post")
router.register('tag',views.Tagviewset,basename="tag")
router.register('comment',views.Commentviewset,basename="comment")



urlpatterns = [
    # https://www.django-rest-framework.org/tutorial/6-viewsets-and-routers/#using-routers
    path('', include(router.urls)),
    
]