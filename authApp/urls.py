from . import views
from django.urls import path

urlpatterns = [
    path('users-list',views.UserListAPIView.as_view(), name='users-list'),
    path('user-detail/<slug:username>',views.UserDetailAPIView.as_view(), name='UserModel-detail'),
    path('register', views.UserRegisterAPIView.as_view(), name="register"),
    # path('login', views.LoginAPIView.as_view(), name="login"),
    # path('user', views.AuthUserAPIView.as_view(), name="user"),
]