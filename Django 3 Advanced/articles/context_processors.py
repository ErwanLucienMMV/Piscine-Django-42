from .forms import MenuAuthenticationForm


def menu_login(request):
    return {"login_form": MenuAuthenticationForm(request=request)}
