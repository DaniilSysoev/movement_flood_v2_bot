from django.contrib import admin
from .models import Profile
from .forms import ProfileForm


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('foreign_id', 'name', 'tg_tag', 'id_channel', 'birthday')
    form = ProfileForm