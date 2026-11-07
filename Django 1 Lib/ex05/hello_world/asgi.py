def create_application():
    import os
    from django.core.asgi import get_asgi_application

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hello_world.settings")
    return get_asgi_application()


application = create_application()
