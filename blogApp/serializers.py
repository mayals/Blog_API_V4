from rest_framework import serializers
from . my_validators import requiredValidator,checkTitleValidator,maxLengthValidator
from rest_framework.validators import UniqueValidator
from.models import Category,Post,Comment
from rest_framework import status
from authApp.models import UserModel




class CategorySerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField(validators=[
                                            maxLengthValidator,
                                            # requiredValidator,# this notwork!
                                            UniqueValidator(queryset=Category.objects.all(),message='يجب أن يكون أسم التصنيف غير مكرر')
                                            ])
    description    = serializers.CharField(required=False) 
    #url - mean -> category detail and use HyperlinkedIdentityField
    url = serializers.HyperlinkedIdentityField(read_only=True, view_name='blogApp:category-detail', lookup_field='slug')   # view_name='{model_name}-detail'
    posts_category  = serializers.HyperlinkedRelatedField(read_only=True, view_name='blogApp:post-detail', many=True, lookup_field='slug')
    

    class Meta:
        model            = Category 
        fields           = ['id','name','description','date_add','date_update','url','posts_category'] 
        read_only_fields = ('id','url','posts_category')
        


    def create(self, validated_data):
        return Category.objects.create(**validated_data)


    # work ok all :) to make "name" not allowed for update
    # https://www.appsloveworld.com/django/100/14/how-to-make-a-field-editable-on-create-and-read-only-on-update-in-django-rest-fra
    def update(self, instance, validated_data):
        print(validated_data)
        instance.name = validated_data.get('name',instance.name)  
        instance.description = validated_data.get('description',instance.description)                           
        super().update(instance, validated_data) # not need
        instance.save()
        return instance 
    
    




class PostSerializer(serializers.HyperlinkedModelSerializer):
    id            = serializers.UUIDField(read_only=True)
    category      = serializers.SlugRelatedField(
                                                queryset = Category.objects.all(),
                                                slug_field = 'name'  # to display category_id asredable  use name field  insead of id field 
                                                ) 
    title         = serializers.CharField(validators=[
                                                    maxLengthValidator,
                                                    # checkTitleValidator, # work ok
                                                    requiredValidator,#not work!
                                                    UniqueValidator(queryset=Post.objects.all())
                                           ])
    author        = serializers.SlugRelatedField(
                                                queryset = UserModel.objects.all(),
                                                slug_field = 'username'  # to display category_id asredable  use name field  insead of id field 
                                                ) 
    body          = serializers.CharField(required=True,style={'base_template': 'textarea.html'} )
    
    
    
    url           = serializers.HyperlinkedIdentityField(read_only=True,view_name='blogApp:post-detail',lookup_field='slug')  
    comments_post = serializers.HyperlinkedRelatedField(read_only=True,view_name='blogApp:comment-detail',many=True)
    
     
    class Meta:
        model            = Post 
        fields           = ['id','category','title','body','author','date_add','date_update','url','comments_post'] 
        read_only_fields = ('id','comments_post','url','likes','tags')


    def create(self, validated_data): # work ok :)
        category_data = validated_data.pop('category')  # validated_data no longer has category
        author_data   = validated_data.pop('author')    # validated_data no longer has author
        post          = Post.objects.create(**validated_data)
        post.category = self.category
        post.author   = self.context['request'].user 
        post.save()
        return post    


   # https://www.django-rest-framework.org/api-guide/serializers/#writable-nested-representations
    def update(self, instance, validated_data): # work ok :)
        
        author_data = validated_data.pop('author')      # validated_data no longer has author
        author = instance.author                        #  author field  will not updaded(not changed) 
        
        # only these 3 fields (title, category & body) will be updated(change)
        instance.category = validated_data.get('category', instance.category)
        instance.title    = validated_data.get('title', instance.title) 
        instance.body     = validated_data.get('body', instance.body)
        super().update(instance, validated_data) # we must update the main class (super)-> (PostSerializer) in order to get right new slug on  a new title
        instance.save()
        return instance
       






class CommentSerializer(serializers.ModelSerializer):
    id            = serializers.UUIDField(read_only=True)    
    post          = serializers.SlugRelatedField(
                                                queryset = Post.objects.all(),
                                                slug_field = 'title' , # to display category_id asredable  use name field  insead of id field 
                                                help_text='choice the post title you want to comment on.',
    )
    comment_by    = serializers.SlugRelatedField(
                                                queryset = UserModel.objects.all(),
                                                slug_field = 'username'  # to display category_id asredable  use name field  insead of id field 
    )  
    text          = serializers.CharField(required=True,
                                          style={'base_template': 'textarea.html'},
                                          help_text='Enter your comment.',
    )
    allowed       = serializers.BooleanField(default=True)
    

    class Meta:
        model  = Comment 
        fields = ['id','post','text','comment_by','allowed'] 
        read_only_fields = ('id',)

    
    def create(self, validated_data): # work ok :)
        print('self =' + str(self))
        print('self.context =' + str(self.context)) # self.context ={'request': <rest_framework.request.Request: POST '/api/blog/comment/'>, 'format': None, 'view': <blogApp.views.Commentviewset object at 0x0000014660FDFD00>} 
        print('self.kwarg =' + str(self.get_extra_kwargs))
        print('validated_data =' + str(validated_data))

        post = validated_data.pop('post')               # validated_data no longer has post
        comment_by = validated_data.pop('comment_by')   # validated_data no longer has comment_by             
        
        comment = Comment.objects.create(**validated_data)
        comment.post = post
        comment.comment_by = self.context['request'].user   
        comment.save()
        return comment    