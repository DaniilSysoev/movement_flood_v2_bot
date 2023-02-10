from django import forms
from .models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = {
            'foreign_id',
            'name',
            'tg_tag',
            'id_channel',
            'birthday'
        }
        widgets = {
            'name': forms.TextInput,
            'tg_tag': forms.TextInput,
            'id_channel': forms.TextInput
        }