from rest_framework import serializers,status



def requiredValidator(value):
    if value is None:
            raise serializers.ValidationError('This field is required',status.HTTP_400_BAD_REQUEST)
    return value



def checkTitleValidator(value):
    if value != "mytitle":
        raise serializers.ValidationError('This field must be mytitle.',status.HTTP_400_BAD_REQUEST)
    return value



def maxLengthValidator(value):
    if len(str(value)) >=20 :
        raise serializers.ValidationError('يجب ان لا يتجاوز طول الخانة عن  20.',status.HTTP_400_BAD_REQUEST)
    return value
