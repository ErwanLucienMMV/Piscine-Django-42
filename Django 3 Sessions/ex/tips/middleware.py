import random
import time

from django.conf import settings


class AnonymousNameMiddleware:
    """Resolve the name before rendering, without extending its fixed lifetime."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            now = time.time()
            name = request.session.get("anonymous_name")
            expires = request.session.get("anonymous_name_expires", 0)
            if name not in settings.ANONYMOUS_NAMES or now >= expires:
                choices = [item for item in settings.ANONYMOUS_NAMES if item != name]
                name = random.choice(choices or settings.ANONYMOUS_NAMES)
                request.session["anonymous_name"] = name
                request.session["anonymous_name_expires"] = now + settings.ANONYMOUS_NAME_LIFETIME
            request.anonymous_name = name
        return self.get_response(request)
