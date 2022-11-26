from django.db import models
from django.urls import reverse
from django.utils.text import slugify
import uuid




#----------------------------------------[  Category  ]----------------------------------------------------#
class Category(models.Model):
    id          = models.UUIDField(primary_key=True, editable=False,default=uuid.uuid4)
    name        = models.CharField(max_length=20, editable=False, unique=True,null=True,blank=False)
    slug        = models.SlugField(max_length=25, blank=True, null=True)
    description = models.TextField(null =True,blank=True)
    date_add    = models.DateTimeField(auto_now=False, auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True,  auto_now_add=False)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('blogApp:category-detail', kwargs = {"slug":self.slug})      #vue view_name='{model_name}-detail'

    def save(self, *args, **kwargs):  
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)  # Call the "real" save() method. 

    
    class Meta:
        ordering =['name']
        verbose_name_plural = "Categories"





#----------------------------------------[  Post  ]----------------------------------------------------#
class Post(models.Model):
    id            = models.UUIDField(primary_key=True, editable=False,default=uuid.uuid4)
    category      = models.ForeignKey(Category,on_delete=models.CASCADE,null=True,blank=False,related_name="posts_category")
    title         = models.CharField(max_length=20, editable=False, null=True,blank=False)
    slug          = models.SlugField(max_length=25, blank=True, null=True)
    author        = models.ForeignKey('authApp.UserModel',on_delete=models.CASCADE,related_name='posts_author',null=True,blank=False)
    body          = models.TextField(null=True,blank=False)
    date_add      = models.DateTimeField(auto_now=False, auto_now_add=True)
    date_update   = models.DateTimeField(auto_now=True,  auto_now_add=False)
    likes         = models.ManyToManyField('authApp.UserModel', related_name='posts_likes', blank=True)
    tags          = models.ManyToManyField('Tag', related_name='posts_tags', blank=True)

    
    def number_of_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title 
    class Meta:
        ordering = ['-date_add', 'author']
        unique_together = ['title', 'author']
        
    def get_absolute_url(self):
        return reverse('blogApp:post-detail', kwargs = {"slug":self.slug})      #vue view_name='{model_name}-detail'    
    
    def save(self, *args, **kwargs):  
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)  # Call the "real" save() method.




#----------------------------------------[  Tag  ]----------------------------------------------------#
class Tag(models.Model):
    id            = models.UUIDField(primary_key=True, editable=False,default=uuid.uuid4)
    word        = models.CharField(max_length=35)
    slug        = models.CharField(max_length=250)
    date_add    = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.word






#----------------------------------------[  Comment  ]----------------------------------------------------#
class Comment(models.Model):
    id          = models.UUIDField(primary_key=True, editable=False,default=uuid.uuid4)
    post        = models.ForeignKey(Post,on_delete=models.CASCADE,null=True,blank=False,related_name="comments_post")
    text        = models.TextField(null=True,blank=False)
    comment_by  = models.ForeignKey('authApp.UserModel',on_delete=models.CASCADE,related_name='comments_author',null=True,blank=False)
    allowed     = models.BooleanField(default=True)
    date_add    = models.DateTimeField(auto_now=False, auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True,  auto_now_add=False)
    
    def __str__(self):
        return f'"{self.text}" by author:{self.comment_by}'

    class Meta:
        ordering = ['-date_add']


