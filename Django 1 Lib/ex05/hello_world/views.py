def hello_world(request):
    from django.http import HttpResponse

    return HttpResponse("Hello World !", content_type="text/plain; charset=utf-8")
