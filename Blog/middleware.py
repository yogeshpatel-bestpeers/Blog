from django.contrib.auth.models import AnonymousUser

from .models import CustomUser


class CustomAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_id = request.session.get("user_id")
        if user_id:
            try:
                request.user = CustomUser.objects.get(id=user_id)
            except CustomUser.DoesNotExist:
                request.user = AnonymousUser()
        else:
            request.user = AnonymousUser()
        return self.get_response(request)
