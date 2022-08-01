from rest_framework.permissions import IsAuthenticated


class ProfilePermission(IsAuthenticated):

    def has_object_permission(self, request, view, obj):
        _permission = bool(request.user == obj or request.user not in obj.blocked or obj not in request.user.blocked)
        return self.has_permission(request, view) and _permission

class SnippetUpdateDeletePermission(IsAuthenticated):

    def has_object_permission(self, request, view, obj):
        return bool(request.user.is_superuser or request.user == obj.author)