from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.views import View
from .forms import LoginForm, RegisterForm, ProfileEditForm
from django.contrib import messages

class LoginView(View):
    def get(self, request):
        form = LoginForm()
        context = {
            'form': form
        }
        return render(request, 'users/login.html', context)

    def post(self, request):
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "You have successfully logged in.")
            return redirect('todo:home')

        else:
            return render(request, 'users/register.html', {'form': form})

class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.info(request, 'You have successfully logged out.')
        return redirect('users:login')

class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'users/register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have successfully registered.')
            return redirect('users:login')

        else:
            return render(request, 'users/register.html', {'form': form})

class ProfileDetail(View):
    def get(self, request):
        context = {
            'user': request.user
        }
        return render(request, 'users/profile.html', context)


class ProfileEdit(View):
    def get(self, request):
        form = ProfileEditForm(instance=request.user)
        return render(request, 'users/profile_edit.html', {'form': form})

    def post(self, request):
        form = ProfileEditForm(instance=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have successfully updated your profile.')
            return redirect('todo:home')

        else:
            return render(request, 'users/profile_edit.html', {'form': form})


