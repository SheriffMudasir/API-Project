from rest_framework import permissions

class IsManagerOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        
        return request.user.groups.filter(name="Manager").exists()
    
class IsManagerDeliverycrewOwner(permissions.BasePermission):
    
    # Allow safe methods for all users
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Only Manager
        if request.user.groups.filter(name="Manager").exists():
            return True
        
        # Allow access if the user is the one who created the order or if the delivery crew is assigned to the order
        if obj.user == request.user or obj.delivery_crew == request.user:
            return True
        return False
        
        
        
    