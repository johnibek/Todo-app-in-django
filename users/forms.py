from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms

class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit)
        user.set_password(self.cleaned_data['password1'])
        user.save()
        return user

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
