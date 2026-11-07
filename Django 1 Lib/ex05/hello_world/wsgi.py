def create_application():
    import os
    from django.core.wsgi import get_wsgi_application

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hello_world.settings")
    return get_wsgi_application()


application = create_application()
