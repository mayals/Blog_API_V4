from . import views
from django.urls import path

urlpatterns = [
    path('register', views.UserRegisterAPIView.as_view(), name="register"),
    path('login', views.UserLoginAPIView.as_view(), name="login"),
    path('current-user', views.AuthUserAPIView.as_view(), name="current-user"),
    
    # only for admin
    path('users-list',views.UserListAPIView.as_view(), name='users-list'),
    path('user-detail/<slug:username>',views.UserDetailAPIView.as_view(), name='UserModel-detail'),
    
]