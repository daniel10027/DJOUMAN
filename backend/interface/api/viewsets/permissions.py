from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAuthenticatedOrCreateOnly(BasePermission):
    """
    Permet POST sans auth (pour register/login) mais impose auth sinon.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.method == "POST" and getattr(view, "allow_post_without_auth", False):
            return True
        return bool(request.user and request.user.is_authenticated)
