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
from .models import UserModel
from django.core.exceptions import ValidationError
from rest_framework.authentication import  TokenAuthentication
from django.shortcuts import get_object_or_404

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes


#----------------------------------------[  UserRegisterAPIView  ]----------------------------------------------------#
# Register - Create new user .. 
class UserRegisterAPIView(GenericAPIView):
    authentication_classes = []
    serializer_class = RegisterSerializer

    #  work ok
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)

        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    # not worl!
    def perform_create(self, serializer):
        queryset = UserModel.objects.filter(username=self.request.user.username)
        if queryset.exists():
            raise ValidationError('You have already signed up')
        serializer.save(user=self.request.user)


    







# https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication
# username and password to get token and login(after i install --> (rest_framework.authtoken) ,token must enter there)
#----------------------------------------[  CustomAuthToken-- Login   ]----------------------------------------------------#
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



#----------------------------------------[  token creat for all users  ]----------------------------------------------------#
#https://www.django-rest-framework.org/api-guide/authentication/#generating-tokens 
# If you've already created some users, you can generate tokens for all existing users like this:
if UserModel.objects.all().exists():
    for user in UserModel.objects.all() :
        Token.objects.get_or_create(user=user)










#----------------------------------------[  UserListAPIView  ]----------------------------------------------------#
# for admin only to see all users and their details
class UserListAPIView(GenericAPIView):
    queryset = UserModel.objects.all()
    serializer_class = RegisterSerializer
    
    # permission_classes = [IsAdminUser]
   
    # get all users
    def get(self, request, format=None): # work ok 
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = RegisterSerializer(queryset, many=True, context={'request': request})
        return response.Response(serializer.data,status=status.HTTP_200_OK)






#----------------------------------------[  UserDetailAPIView  ]----------------------------------------------------#
class UserDetailAPIView(GenericAPIView): # 
    queryset = UserModel.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = 'username'
    
    # get selected user by its username
    def get(self, request, username, format=None):# only get is work ok with Token AUTH.another methods not work !
        # user = self.get_object()
        user = UserModel.objects.get(username=username)
        serializer = RegisterSerializer(user, many=False, context = {'request': request})
        return response.Response(serializer.data,status=status.HTTP_200_OK)
   



# https://medium.com/codex/implementing-a-rest-api-with-django-rest-framework-41999c96fcd6
#----------------------------------------[  'PUT','DELETE'   ]----------------------------------------------------#
# for methods get-update-delete 
@api_view(http_method_names=['GET','PUT','DELETE']) # all work ok with auth token :)
@permission_classes((IsAuthenticated, ))
def user_update_delete(request, username):
        try:
            user = UserModel.objects.get(username=username)
        except UserModel.DoesNotExist:
            return response.Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':   #  GET is work ok with Token AUTH :)
            user_serializer = RegisterSerializer(user, context={'request': request})
            return response.Response(user_serializer.data,status=status.HTTP_200_OK)
        
        elif request.method == 'PUT':   #  PUT is work ok with Token AUTH :)
            user_serializer = RegisterSerializer(user, data=request.data, context={'request': request})
            if user_serializer.is_valid():
                user_serializer.save()
                return response.Response(user_serializer.data,status=status.HTTP_200_OK)
            return response.Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        elif request.method == 'DELETE': # DELETE is work ok with Token AUTH :)
            user.delete()
            return response.Response(status=status.HTTP_204_NO_CONTENT)




    # def update(self, request, username, format=None): #not work {"detail":"Method \"PUT\" not allowed."}
    #     # user = self.get_object()
    #     user = UserModel.objects.get(username=username)
    #     serializer = RegisterSerializer(user, data= request.data, context = {'request': request})
    #     if serializer.is_valid():
    #         serializer.save()
    #         return response.Response(serializer.data, status = status.HTTP_200_OK)   
    #     return response.Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
 
   


    # #     return super(UserDetailAPIView,self).get_object()
    # def update(self, request,*args,**kwargs): #not work {"detail":"Method \"PUT\" not allowed."}
    #     username = kwargs.get('username')
    #     user = get_object_or_404(UserModel, username=username)
    #     serializer = RegisterSerializer(user, data= request.data, context = {'request': request})
    #     if serializer.is_valid():
    #         serializer.save()
    #         return response.Response(serializer.data, status = status.HTTP_200_OK)   
    #     return response.Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
 


     


    # def update(self, request, *args, **kwargs): #not work {"detail":"Method \"PUT\" not allowed."}
    #     partial = kwargs.pop('partial', False)
    #     username = self.kwargs.get("username")
    #     instance = get_object_or_404(UserModel, username=username)
    #     serializer = self.get_serializer(instance, data=request.data)
    #     if serializer.is_valid(raise_exception=True):
    #         self.perform_update(serializer)
    #         return response.Response(serializer.data,status=status.HTTP_200_OK)
    #     return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



    
    # def update(self,request,kwargs):#not work {"detail":"Method \"PUT\" not allowed."}
    #     username = kwargs.get('username')
    #     user = UserModel.objects.get(username=username)
    #     serializer = RegisterSerializer(user, 
    #                                             email      = request.data['email'],
    #                                             first_name = request.data['first_name'],
    #                                             last_name  = request.data['last_name'],
    #                                             gender     = request.data['gender'],
    #                                             born_date  = request.data['born_date'],
    #                                             country    = request.data['country'],
    #                                             avatar     = request.data['avatar'],
    #                                             bio        = request.data['bio'],
    #                                             website    = request.data['website']
    #     )
    #     if serializer.is_valid():
    #         self.perform_update(serializer)
    #         return response.Response(serializer.data,status=status.HTTP_200_OK)
    #     return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    # def update(self, request, *args, **kwargs):
    #     partial = kwargs.pop('partial', False)
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, email      = request.data['email'],
    #                                             first_name = request.data['first_name'],
    #                                             last_name  = request.data['last_name'],
    #                                             gender     = request.data['gender'],
    #                                             born_date  = request.data['born_date'],
    #                                             country    = request.data['country'],
    #                                             avatar     = request.data['avatar'],
    #                                             bio        = request.data['bio'],
    #                                             website    = request.data['website'])
    #     if serializer.is_valid(raise_exception=True):
    #         self.perform_update(serializer)
    #         return response.Response(serializer.data,status=status.HTTP_200_OK)
    #     return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)







 # get requst user (current-user)
    # https://www.django-rest-framework.org/api-guide/serializers/#absolute-and-relative-urls
   # https://www.django-rest-framework.org/api-guide/generic-views/#genericapiview
# get requst user (only current-user can view)
#----------------------------------------[  ProfileUserAPIView  ]----------------------------------------------------#
class ProfileUserAPIView(GenericAPIView): # not work :(
    serializer_class = RegisterSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication)

    def get_object(self,request):
        try:
            user = self.request.user
        except UserModel.DoesNotExist:
            return response.Response(status=status.HTTP_404_NOT_FOUND)

     # get selected user by its username
    # def get(self, request):
    #     try:
    #         user = request.user
    #         serializer = RegisterSerializer(user,many=False)
    #         return response.Response(serializer.data,status=status.HTTP_200_OK)
        
    #     except UserModel.DoesNotExist:
    #         return response.Response(status=status.HTTP_404_NOT_FOUND)
        
    def get(self, request):
        user = request.user
        serializer = RegisterSerializer(user)
        return response.Response({'user': serializer.data})    
       
    # def perform_update(self,request):
    #     user = self.request.user
    #     serializer = RegisterSerializer(user, 
    #                                             email      = request.data['email'],
    #                                             username   = request.data['username'],
    #                                             first_name = request.data['first_name'],
    #                                             last_name  = request.data['last_name'],
    #                                             gender     = request.data['gender'],
    #                                             born_date  = request.data['born_date'],
    #                                             country    = request.data['country'],
    #                                             avatar     = request.data['avatar'],
    #                                             bio        = request.data['bio'],
    #                                             website    = request.data['website']
    #     )
    #     if serializer.is_valid():
    #         serializer.save()
    #         return response.Response(serializer.data)
    #     return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)







# not using now because login without token (bad login same as BasicAuthentication ) 
# Login - login user before token installed.. 
# username and password login(before i install --> (rest_framework.authtoken) ,so no token ther)
#----------------------------------------[  UserLoginAPIView  ]----------------------------------------------------#
class UserLoginAPIView(GenericAPIView): #  work but not need  because we are token auth not bascic auth
    serializer_class = LoginSerializer

    def post(self, request):
        username = request.data.get('username', None)
        password = request.data.get('password', None)
        user = authenticate(username=username, password=password)
        if user:
            serializer = self.serializer_class(user)
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        return response.Response({'message': "Invalid credentials, please try again"}, status=status.HTTP_401_UNAUTHORIZED)



