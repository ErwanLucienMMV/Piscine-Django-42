from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Tip, User, Vote

admin.site.register(User, UserAdmin)


class VoteInline(admin.TabularInline):
    model = Vote
    extra = 0


@admin.register(Tip)
class TipAdmin(admin.ModelAdmin):
    list_display = ("content", "author", "date")
    search_fields = ("content", "author__username")
    list_filter = ("date",)
    inlines = (VoteInline,)
