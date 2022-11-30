from django.shortcuts import render
from.models import Category,Post,Comment,Tag
from.serializers import CategorySerializer,PostSerializer,CommentSerializer,TagSerializer
from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import authentication



# POST       method work ok  :) 
# GET        method work ok  :)
# GET-Detail method work ok  :)
# PUT        method work ok  :)
# DELETE     method work ok  :)
class Categoryviewset(viewsets.ModelViewSet): 
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "slug"
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes     = [permissions.IsAuthenticatedOrReadOnly]
    



 
# POST       method work ok  :) 
# GET        method work ok  :)
# GET-Detail method work ok  :)
# PUT        method work ok  :)
# DELETE     method work ok  :)  
class Postviewset(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = "slug"
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes     = [permissions.IsAuthenticatedOrReadOnly]


 
# POST       method work ok  :) 
# GET        method work ok  :)
# GET-Detail method work ok  :)
# PUT        method work ok  :)
# DELETE     method work ok  :) 
class Tagviewset(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_field = "slug"
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes     = [permissions.IsAdminUser]



 
# POST       method work ok  :) 
# GET        method work ok  :)
# GET-Detail method work ok  :)
# PUT        method work ok  :)
# DELETE     method work ok  :) 
#  all work but wrong url :, must be nested url
class Commentviewset(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    
    serializer_class = CommentSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes     = [permissions.IsAuthenticatedOrReadOnly]

