from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.db.models import Count, OuterRef, Q, Subquery
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST, require_http_methods

from .forms import RegistrationForm, TipForm
from .models import Tip, Vote


@require_http_methods(["GET", "POST"])
def home(request):
    form = TipForm(request.POST if request.method == "POST" else None)
    if request.method == "POST":
        if not request.user.is_authenticated:
            raise PermissionDenied
        if form.is_valid():
            tip = form.save(commit=False)
            tip.author = request.user
            tip.save()
            return redirect("home")
    tips = Tip.objects.select_related("author").annotate(
        upvote_count=Count("votes", filter=Q(votes__value=Vote.UP)),
        downvote_count=Count("votes", filter=Q(votes__value=Vote.DOWN)),
    )
    if request.user.is_authenticated:
        tips = tips.annotate(current_vote=Subquery(
            Vote.objects.filter(tip=OuterRef("pk"), user=request.user).values("value")[:1]
        ))
        may_delete = request.user.has_perm("tips.delete_tip")
        may_downvote = request.user.has_perm("tips.downvote_tip")
        for tip in tips:
            tip.may_delete = tip.author_id == request.user.pk or may_delete
            tip.may_downvote = tip.author_id == request.user.pk or may_downvote
    return render(request, "tips/home.html", {"form": form, "tips": tips})


@require_POST
@login_required
def vote(request, pk, direction):
    if direction not in ("up", "down"):
        raise PermissionDenied
    value = Vote.UP if direction == "up" else Vote.DOWN
    with transaction.atomic():
        tip = get_object_or_404(Tip.objects.select_for_update(), pk=pk)
        if value == Vote.DOWN and not request.user.can_downvote_tip(tip):
            raise PermissionDenied
        previous = Vote.objects.filter(tip=tip, user=request.user).first()
        if previous and previous.value == value:
            previous.delete()
        elif previous:
            previous.value = value
            previous.save(update_fields=["value"])
        else:
            Vote.objects.create(tip=tip, user=request.user, value=value)
    return redirect("home")


@require_POST
@login_required
def delete_tip(request, pk):
    tip = get_object_or_404(Tip, pk=pk)
    if not request.user.can_delete_tip(tip):
        raise PermissionDenied
    tip.delete()
    return redirect("home")


@require_http_methods(["GET", "POST"])
def register(request):
    if request.user.is_authenticated:
        return redirect("home")
    form = RegistrationForm(request.POST if request.method == "POST" else None)
    if request.method == "POST" and form.is_valid():
        login(request, form.save())
        return redirect("home")
    return render(request, "tips/auth.html", {"form": form, "title": "Register"})


@require_http_methods(["GET", "POST"])
def sign_in(request):
    if request.user.is_authenticated:
        return redirect("home")
    form = AuthenticationForm(request, data=request.POST if request.method == "POST" else None)
    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        return redirect("home")
    return render(request, "tips/auth.html", {"form": form, "title": "Log in"})


@require_POST
def sign_out(request):
    logout(request)
    return redirect("home")
