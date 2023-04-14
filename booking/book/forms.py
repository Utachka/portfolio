from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    # добавьте любые дополнительные поля, которые вы хотите, чтобы пользователи заполняли
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

class PathDateForm(forms.Form):
    first_date = forms.DateField(label='Выберите дату с')
    second_date = forms.DateField(label='Выберите дату по')
    from_country = forms.CharField(label='Откуда', widget=forms.TextInput(attrs={'class': 'form-control'}))
    to_country = forms.CharField(label='Куда', widget=forms.TextInput(attrs={'class': 'form-control'}))