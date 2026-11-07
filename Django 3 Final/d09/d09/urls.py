from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

from account.views import account

urlpatterns = [
    path("", RedirectView.as_view(url="/account", permanent=False)),
    path("account", account, name="account"),
    path("chat/", include("chat.urls")),
    path("admin/", admin.site.urls),
]
