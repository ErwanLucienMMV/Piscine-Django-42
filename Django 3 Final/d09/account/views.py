from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


@require_http_methods(["GET", "POST"])
def account(request):
    if request.method == "GET":
        return render(request, "account/account.html", {"form": AuthenticationForm(request)})

    action = request.POST.get("action")
    if action == "login":
        form = AuthenticationForm(request, data=request.POST)
        if not form.is_valid():
            return JsonResponse({"errors": form.errors.get_json_data()}, status=400)
        login(request, form.get_user())
    elif action == "logout":
        session_key = request.session.session_key
        logout(request)
        if session_key:
            async_to_sync(get_channel_layer().group_send)(
                "session." + session_key, {"type": "session.logout"}
            )
    else:
        return JsonResponse({"errors": {"__all__": [{"message": "Unknown action."}]}}, status=400)

    return JsonResponse({
        "authenticated": request.user.is_authenticated,
        "username": request.user.get_username() if request.user.is_authenticated else "",
        "csrfToken": get_token(request),
    })
