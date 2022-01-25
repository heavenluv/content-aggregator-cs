import datetime

from django import forms

from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm

from podcasts.models import Category, User


queryset_genre = Category.objects.all()
GENRES_CHOICES = [(obj.id, obj.title) for obj in queryset_genre]
# GENRES_CHOICES = [
#     (1,'Python'),
#     (3,'Backend'),
#     (4,'Frontend'),
#     (5,'Data Science'),
#     (6,'Machine Learning'),
# ]
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ("email",)

class GenreSelectionForm(forms.Form):
    available_options = forms.MultipleChoiceField(
        required=True, widget=forms.CheckboxSelectMultiple, choices=GENRES_CHOICES)
