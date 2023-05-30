from rest_framework.permissions import BasePermission


class CustomPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False  # User is not authenticated, permission denied

        if user.role == 'admin' and request.method in ['GET', 'POST', 'PUT', 'DELETE']:
            return True  # Admin has access to all request methods

        if user.role == 'agent' and request.method in ['GET', 'POST']:
            return True  # Agent has access to GET and POST methods

        if user.role == 'customer' and request.method == 'GET':
            return True  # User has access to only the GET method

        return False



# class IsGetRequest(BasePermission):
#     def has_permission(self, request, view):
#         return request.method == 'GET' or request.method == 'POST'
