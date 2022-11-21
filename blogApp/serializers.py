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
    
 
    # not work ..no chage has done in message!
    # https://www.django-rest-framework.org/api-guide/serializers/#field-level-validation
    # def validate_name(self,value):
    #     if value is None:
    #         raise serializers.ValidationError("This field is required",status.HTTP_400_BAD_REQUEST)
    #     return value

    def create(self, validated_data):
        return Category.objects.create(**validated_data)


    # work ok all :) to make "name" not allowed for update
    # https://www.appsloveworld.com/django/100/14/how-to-make-a-field-editable-on-create-and-read-only-on-update-in-django-rest-fra
    def update(self, instance, validated_data):
        validated_data.pop('name')  # validated_data no longer has name 
        instance.description = validated_data.get('description',instance.description)                           
        instance.save()
        super().update(instance, validated_data)
        raise serializers.ValidationError("This field - Name - not allowed to update",status.HTTP_400_BAD_REQUEST) 
         

    class Meta:
        model            = Category 
        fields           = ['id','name','description','date_add','date_update','url','posts_category'] 
        read_only_fields = ('id','url')
        # extra_kwargs     = {
        #                     "name": {
        #                         "error_messages": { "required": "Please This field is required" },
        #                         "max_length": 20  
        #                     }
        # }

        # extra_kwargs = {
        #             'name' : {'required' : True },
        #             'id'   : {'read_only': True },
        #             'slug' : {'read_only': True },
        #             'posts_category': {
        #                       'read_only'    : True,
        #                       'view_name'    : 'post-detail',
        #                       'lookup_field' : 'slug' 
        #                     },
                    
       
        #             'url'  : {
        #                        'read_only'    : True,
        #                        'view_name'    : 'category-detail',
        #                        'lookup_field' : 'slug'     
        #                     },                      
        #             }








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
    comments_post = serializers.HyperlinkedRelatedField(read_only=True,view_name='comment-detail',many=True)
    
     
    class Meta:
        model            = Post 
        fields           = ['id','category','title','body','author','date_add','date_update','url','comments_post'] 
        read_only_fields = ('id','comments_post','url')


    


    def create(self, validated_data):
        author_data = validated_data.pop('author')   # validated_data no longer has author
        post = Post.objects.create(**validated_data)
        Post.objects.create(post=post, **author_data)
        return post    


    # work ok all :) to make "name" not allowed for update
    # https://www.appsloveworld.com/django/100/14/how-to-make-a-field-editable-on-create-and-read-only-on-update-in-django-rest-fra
    def update(self, instance, validated_data):
        validated_data.pop('title') # validated_data no longer has title
        validated_data.pop('author')# validated_data no longer has author
        instance.category = validated_data.get('category',instance.category)                           
        instance.body = validated_data.get('body',instance.body)
        instance.save()
        super().update(instance, validated_data)
        raise serializers.ValidationError("This field - title - not allowed to update",status.HTTP_400_BAD_REQUEST) 






class CommentSerializer(serializers.HyperlinkedModelSerializer):
    id            = serializers.UUIDField(read_only=True)    
    post          = serializers.SlugRelatedField(
                                                queryset = Post.objects.all(),
                                                slug_field = 'title'  # to display category_id asredable  use name field  insead of id field 
    ) 
    
    text          = serializers.CharField(required=True,style={'base_template': 'textarea.html'} ) 
    comment_by    = serializers.CharField(required=True)
    allowed       = serializers.BooleanField(default=False)
    

    class Meta:
        model  = Comment 
        fields = ['id','post','text','comment_by','allowed'] 