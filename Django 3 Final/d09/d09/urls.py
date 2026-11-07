from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView

from account.views import account

urlpatterns = [
    path("", RedirectView.as_view(url="/account", permanent=False)),
    path("account", account, name="account"),
    path("admin/", admin.site.urls),
]
