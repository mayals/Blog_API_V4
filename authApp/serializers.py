from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from.models import UserModel
from rest_framework import status
from rest_framework.request import Request

# https://www.django-rest-framework.org/tutorial/5-relationships-and-hyperlinked-apis/#hyperlinking-our-api
# https://www.django-rest-framework.org/api-guide/validators/#uniquevalidator
# https://www.django-rest-framework.org/api-guide/relations/
# https://medium.com/django-rest/django-rest-framework-login-and-register-user-fd91cf6029d5



##############################################[ RegisterSerializer ]############################################################
class RegisterSerializer(serializers.HyperlinkedModelSerializer):
    username = serializers.CharField(required=True,
                                     help_text='username must be uniqe.',
                                     style={'placeholder': 'username here ..'},
                                     validators=[UniqueValidator(queryset=UserModel.objects.all())]
    )
    email = serializers.EmailField(
                                    required=True,
                                    style={'placeholder': 'email here ..'},
                                    help_text='Enter correct email.',
                                    validators=[UniqueValidator(queryset=UserModel.objects.all())]
    )
    password  = serializers.CharField(max_length=16, 
                                      min_length=8, 
                                      write_only=True,
                                      required=True,
                                      help_text='Password must be more than 8 Characters.',
                                      style={'input_type': 'password', 'placeholder': 'Password'}
    )
    password2 = serializers.CharField(max_length=16, 
                                      min_length=8, 
                                      write_only=True,
                                      required=True,
                                      help_text='Password must be more than 8 Characters.',
                                      style={'input_type': 'password', 'placeholder': 'Password2'}
    )
    url = serializers.HyperlinkedIdentityField(read_only=True,
                                               view_name='authApp:UserModel-detail',
                                               lookup_field='username',
                                              
    )
    posts_author =  serializers.HyperlinkedRelatedField(read_only=True,
                                                        view_name='blogApp:post-detail', 
                                                        many=True,
                                                        lookup_field='slug'
    )
    comments_author =  serializers.HyperlinkedRelatedField(read_only=True,
                                                        view_name='blogApp:comment-detail', 
                                                        many=True,
                                                        lookup_field='slug'
    )
    

    class Meta:
        model  = UserModel 
        fields = [
            'username','email','password','password2',
            'first_name','last_name','gender','born_date','country','avatar','bio','website',
            'url','posts_author','comments_author','favorites'
        ]
        write_only_fields = ['password','password2']
        read_only_fields = ['url','posts_author','comments_author',]
        # extra_kwargs = {'password': {'write_only': True}}
        
        extra_kwargs = {
                        'url': {   
                                'view_name'   : 'UserModel-detail', 
                                'lookup_field': 'username'
                               },
            # 'users': {'lookup_field': 'username'}
        }


    
    def validate_username(self, value): # work ok :)
        if value is None:
            raise serializers.ValidationError("username field is required",status.HTTP_400_BAD_REQUEST)
        if UserModel.objects.filter(username=value).exists() == True:
            raise serializers.ValidationError(f" '{value}'  this username already been used. Try another username.",status.HTTP_400_BAD_REQUEST) 
        return value # the output here is validated username only
    

    def validate_email(self, value): # work ok :)
        if value is None:
            raise serializers.ValidationError("email field is required",status.HTTP_400_BAD_REQUEST)
        if UserModel.objects.filter(email=value).exists() == True:
            raise serializers.ValidationError(f" '{value}'  this email already been used. Try another email.",status.HTTP_400_BAD_REQUEST)
        return value # the output here is validated email only
    

    def validate(self, data): # work ok :)
        if data['password'] is None:
            raise serializers.ValidationError("password field is required",status.HTTP_400_BAD_REQUEST)
        if data['password2'] is None:
            raise serializers.ValidationError("password2 field is required",status.HTTP_400_BAD_REQUEST)
        if len(data['password']) < 8:
             raise serializers.ValidationError('Password must be  more than 8 Characters.',status.HTTP_400_BAD_REQUEST)
        if data['password'] != data['password2']:
            raise serializers.ValidationError('Password and Confirm Password Should be Same!',status.HTTP_400_BAD_REQUEST)  
        return data # the output here is validated data only
       
    # https://www.django-rest-framework.org/api-guide/serializers/#handling-saving-related-instances-in-model-manager-classes
    # https://www.django-rest-framework.org/api-guide/serializers/#additional-keyword-arguments
    # https://github.com/LondonAppDev/course-rest-api/blob/master/src/profiles_project/profiles_api/serializers.py


    def create(self, validated_data):
        user = UserModel(
                        email      = validated_data['email'],
                        username   = validated_data['username'],
                        first_name = validated_data['first_name'],
                        last_name  = validated_data['last_name'],
                        gender     = validated_data['gender'],
                        born_date  = validated_data['born_date'],
                        country    = validated_data['country'],
                        avatar     = validated_data['avatar'],
                        bio        = validated_data['bio'],
                        website    = validated_data['website']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


    
    

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name  = validated_data.get('last_name', instance.last_name)
        instance.gender     = validated_data.get('gender', instance.gender)
        instance.born_date  = validated_data.get('born_date', instance.born_date)
        instance.country    = validated_data.get('country', instance.country)
        instance.avatar     = validated_data.get('avatar', instance.avatar)
        instance.website    = validated_data.get('website', instance.website)
        instance.bio        = validated_data.get('bio', instance.bio)
        instance.save()
        user = UserModel(instance)
        return user

        

    
##############################################[ LoginSerializer ]############################################################
class LoginSerializer(serializers.ModelSerializer):

    username = serializers.CharField(required=True,
                                     style={'placeholder': 'username here ..'},
                                     help_text='Enter your username.',
                                     validators=[UniqueValidator(queryset=UserModel.objects.all())]
    )
    password  = serializers.CharField(
                                      max_length=16, 
                                      min_length=8, 
                                      write_only=True,
                                      required=True,
                                      help_text='Enter your password.',
                                      style={'input_type': 'password', 'placeholder': 'password here ..'}
    )
    class Meta:
        model = UserModel
        fields = ('username', 'password')

        # read_only_fields = ['token']



#---------------------------------------[ ProfileSerializer ]------------------------------------
class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    
    email = serializers.EmailField(
                                    required=True,
                                    style={'placeholder': 'email here ..'},
                                    help_text='Enter correct email.',
                                    validators=[UniqueValidator(queryset=UserModel.objects.all())]
    )
    
    url = serializers.HyperlinkedIdentityField(read_only=True,
                                               view_name='authApp:UserModel-detail',
                                               lookup_field='username',
                                              
    )
    posts_author =  serializers.HyperlinkedRelatedField(read_only=True,
                                                        view_name='blogApp:post-detail', 
                                                        many=True,
                                                        lookup_field='slug'
    )
    comments_author =  serializers.HyperlinkedRelatedField(read_only=True,
                                                        view_name='blogApp:comment-detail', 
                                                        many=True,
                                                        lookup_field='slug'
    )
    

    class Meta:
        model  = UserModel 
        fields = [
            'email','first_name','last_name','gender','born_date','country','avatar','bio','website',
            'url','posts_author','comments_author','favorites'
        ]
        read_only_fields = ['url','posts_author','comments_author',]
        # extra_kwargs = {'password': {'write_only': True}}
        
        extra_kwargs = {
                        'url': {   
                                'view_name'   : 'UserModel-detail', 
                                'lookup_field': 'username'
                               },
            # 'users': {'lookup_field': 'username'}
        }


    def validate_email(self, value): # work ok :)
        if value is None:
            raise serializers.ValidationError("email field is required",status.HTTP_400_BAD_REQUEST)
        if UserModel.objects.filter(email=value).exists() == True:
            raise serializers.ValidationError(f" '{value}'  this email already been used. Try another email.",status.HTTP_400_BAD_REQUEST)
        return value # the output here is validated email only


    def update(self, instance, validated_data): # work ok 
        instance.email      = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name  = validated_data.get('last_name', instance.last_name)
        instance.gender     = validated_data.get('gender', instance.gender)
        instance.born_date  = validated_data.get('born_date', instance.born_date)
        instance.country    = validated_data.get('country', instance.country)
        instance.avatar     = validated_data.get('avatar', instance.avatar)
        instance.website    = validated_data.get('website', instance.website)
        instance.bio        = validated_data.get('bio', instance.bio)
        instance.save()
        user = UserModel(instance)
        return user

