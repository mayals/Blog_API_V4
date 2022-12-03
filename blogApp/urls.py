from django.urls import path
from blogApp import views
from rest_framework.urlpatterns import format_suffix_patterns




# Categoryviewset ######################################################
category_list = views.Categoryviewset.as_view({
    'get': 'list',
    'post': 'create'
})
category_detail = views.Categoryviewset.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})




# Postviewset ######################################################
post_list = views.Postviewset.as_view({
    'get' : 'list',
    'post': 'create'
})
post_detail = views.Postviewset.as_view({
    'get'   : 'retrieve',
    'put'   : 'update',
    'patch' : 'partial_update',
    'delete': 'destroy'
})




# Tagviewset ######################################################
tag_list = views.Tagviewset.as_view({
    'get' : 'list',
    'post': 'create'
})
tag_detail = views.Tagviewset.as_view({
    'get'   : 'retrieve',
    'put'   : 'update',
    'patch' : 'partial_update',
    'delete': 'destroy'
})




# Commentviewset ######################################################
comment_list = views.Commentviewset.as_view({
    'get' : 'list',
    'post': 'create'
})
comment_detail = views.Commentviewset.as_view({
    'get'   : 'retrieve',
    'put'   : 'update',
    'patch' : 'partial_update',
    'delete': 'destroy'
})











app_name = 'blogApp'
urlpatterns = format_suffix_patterns([
    # Categoryviewset
    path('category_list/', category_list, name='category-list'),
    path('category_detail/<slug:slug>/', category_detail, name='category-detail'),
    
    # Postviewset
    path('post_list/', post_list, name='post-list'),
    path('post_detail/<slug:slug>/', post_detail, name='post-detail'),

    # Tagviewset
    path('tag_list/', tag_list, name='tag-list'),
    path('tag_detail/<slug:slug>/', tag_detail, name='tag-detail'),

    # Commentviewset
    path('comment_list/', comment_list, name='comment-list'),
    path('comment_detail/<str:id>/', comment_detail, name='comment-detail'),
])









# router = DefaultRouter()
# router.register('category',views.Categoryviewset,basename="category")
# router.register('post',views.Postviewset,basename="post")
# router.register('tag',views.Tagviewset,basename="tag")
# router.register('comment',views.Commentviewset,basename="comment")



# urlpatterns = [
#     # https://www.django-rest-framework.org/tutorial/6-viewsets-and-routers/#using-routers
#     path('', include(router.urls)),
    
# ]