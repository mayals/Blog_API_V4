from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework import response, status, permissions
from .serializers import RegisterSerializer,LoginSerializer
from .models import UserModel
from rest_framework.permissions import IsAdminUser
from django.http import Http404
from django.contrib.auth import authenticate

# https://www.django-rest-framework.org/api-guide/authentication/#by-exposing-an-api-endpoint
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

# https://www.django-rest-framework.org/api-guide/generic-views/#genericapiview
# get requst user (only current-user can view)
class AuthUserAPIView(GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (permissions.IsAuthenticated,)

    # get requst user (current-user)
    # https://www.django-rest-framework.org/api-guide/serializers/#absolute-and-relative-urls
    def get(self, request):
        user = request.user
        serializer = RegisterSerializer(user, many=False, context={'request': request})
        # return response.Response({'user': serializer.data}) -- also work
        return response.Response(serializer.data,status=status.HTTP_200_OK)
    

# Register - Create new user .. 
class UserRegisterAPIView(GenericAPIView):
    authentication_classes = []
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)

        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# not using now because login without token (bad login same as BasicAuthentication ) 
# Login - login user before token installed.. 
# username and password login(before i install --> (rest_framework.authtoken) ,so no token ther)
class UserLoginAPIView(GenericAPIView):
    authentication_classes = []
    serializer_class = LoginSerializer

    def post(self, request):
        username = request.data.get('username', None)
        password = request.data.get('password', None)
        user = authenticate(username=username, password=password)
        if user:
            serializer = self.serializer_class(user)
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        return response.Response({'message': "Invalid credentials, please try again"}, status=status.HTTP_401_UNAUTHORIZED)


# https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication
# username and password to get token and login(after i install --> (rest_framework.authtoken) ,token must enter there)
class CustomAuthToken(ObtainAuthToken):
        
    def post(self, request, *args, **kwargs):
        # print(self.serializer_class) 
        # <class 'rest_framework.authtoken.serializers.AuthTokenSerializer'>
        serializer = self.serializer_class(data=request.data,context={'request': request})                                       
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return response.Response({
                                'token': token.key,
                                'user_id': user.pk,
                                'user_username': user.username,
                                'email': user.email,
                                'message': 'you are now login by way called :TokenAuthentication , using --> rest_framework.authtoken'
        })




#https://www.django-rest-framework.org/api-guide/authentication/#generating-tokens 
# If you've already created some users, you can generate tokens for all existing users like this:
for user in UserModel.objects.all():
    Token.objects.get_or_create(user=user)
        


###############################################################################
 # for admin only to see all users and their details
class UserListAPIView(GenericAPIView):
    queryset = UserModel.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [IsAdminUser]
   
    # get all users
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

     # get selected user by its username
    def get(self, request, username, format=None):
            user = self.get_object(username)
            serializer = RegisterSerializer(user, many=False, context = {'request': request})
            return response.Response(serializer.data,status=status.HTTP_200_OK)