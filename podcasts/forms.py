import datetime

from django import forms

from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm

from podcasts.models import Category

queryset_genre = Category.objects.all().distinct()
print(queryset_genre)
GENRES_CHOICES = [(obj.id, obj.title) for obj in queryset_genre]

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email",)

class GenreSelectionForm(forms.Form):
    available_options = forms.MultipleChoiceField(required=True, widget=forms.CheckboxSelectMultiple, choices=GENRES_CHOICES)
