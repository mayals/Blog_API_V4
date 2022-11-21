from . import views
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token



urlpatterns = [
    path('register/', views.UserRegisterAPIView.as_view(), name="register"),
    # username and password login(before i install --> (rest_framework.authtoken) ,so no token ther)
    path('login/', views.UserLoginAPIView.as_view(), name="login"),
    path('current-user/', views.AuthUserAPIView.as_view(), name="current-user"),

   
    # https://www.django-rest-framework.org/api-guide/authentication/# by-exposing-an-api-endpoint
    # this end point is:(rest_framework.authtoken.views.obtain_auth_token) --> that ask for username and password to give us token
    path('api-token-auth/', obtain_auth_token, name ='api-token-auth'),

    # https://www.django-rest-framework.org/api-guide/authentication/#by-exposing-an-api-endpoint
    # If you need a customized version of the obtain_auth_token view,  to login by token :
    path('login-api-token-auth/', views.CustomAuthToken.as_view(), name ='login-api-token-auth'),

    # only for admin
    path('users-list/',views.UserListAPIView.as_view(), name='users-list'),
    path('user-detail/<slug:username>/',views.UserDetailAPIView.as_view(), name='UserModel-detail'),
    
]