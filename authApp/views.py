from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework import response, status, permissions
from .serializers import RegisterSerializer
from .models import UserModel
from rest_framework.permissions import IsAdminUser
from django.http import Http404


# https://www.django-rest-framework.org/api-guide/generic-views/#genericapiview
class AuthUserAPIView(GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (permissions.IsAuthenticated,)

    # get requst user
    # https://www.django-rest-framework.org/api-guide/serializers/#absolute-and-relative-urls
    def get(self, request):
        user = request.user
        serializer = RegisterSerializer(user, many=False, context={'request': request})
        # return response.Response({'user': serializer.data}) -- also work
        return response.Response(serializer.data,status=status.HTTP_200_OK)
    


class UserRegisterAPIView(GenericAPIView):
    authentication_classes = []
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)

        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserListAPIView(GenericAPIView):
    queryset = UserModel.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'username'

    def get(self, request, format=None):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = RegisterSerializer(queryset, many=True, context={'request': request})
        return response.Response(serializer.data,status=status.HTTP_200_OK)


class UserDetailAPIView(GenericAPIView):
    queryset = UserModel.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'username'

    def get_object(self,username):
        try:
            return UserModel.objects.get(username=username)
        except UserModel.DoesNotExist:
            raise Http404

    
    def get(self, request, username, format=None):
            user = self.get_object(username)
            serializer = RegisterSerializer(user, context = {'request': request})
            return response.Response(serializer.data,status=status.HTTP_200_OK)