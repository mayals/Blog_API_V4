from rest_framework.permissions  import BasePermission,SAFE_METHODS


# https://github.com/encode/django-rest-framework/blob/master/rest_framework/permissions.py#L142
# https://testdriven.io/blog/custom-permission-classes-drf/#:~:text=Safe%20methods%20are%20defined%20in%20rest_framework%2Fpermissions.py%3A%20SAFE_METHODS%20%3D,on%20the%20object%3B%20they%20can%20only%20read%20it.
class IsAuthorOrReadOnly(BasePermission):
    """
    The request is authenticated user is post author's or is a read-only request.
    """

    
    def has_object_permission(self, request, view ,obj):
        return bool(
            request.method in SAFE_METHODS
            or
            request.user == obj.author   
        )
        
    
    # also work ok :)
    # def has_permission(self, request, view ,obj):
    #     if request.method in SAFE_METHODS :
    #         return True
    #     return bool(request.user == obj.author)   
    