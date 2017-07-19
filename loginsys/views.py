from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout

# Create your views here.


def user_registration(request):
    if request.method == 'POST':
        filled_form = UserCreationForm(request.POST)
        if filled_form.is_valid():
            filled_form.save()
            new_user = authenticate(username=filled_form.cleaned_data['username'],
                                    password=filled_form.cleaned_data['password1'])
            login(request, new_user)
            return redirect('/')
        else:
            form = filled_form
    else:
        form = UserCreationForm()
    template = 'loginsys/user_registration.html'
    context = {'form': form}
    return render(request, template, context)


def user_login(request):
    if request.method == 'POST':
        filled_form = AuthenticationForm(request, request.POST)
        if filled_form.is_valid():
            user = authenticate(username=filled_form.cleaned_data['username'],
                                password=filled_form.cleaned_data['password'])
            login(request, user)
            return redirect('/')
        else:
            form = filled_form
    else:
        form = AuthenticationForm(request)
    template = 'loginsys/user_login.html'
    context = {'form': form}
    return render(request, template, context)


def user_logout(request):
    logout(request)
    return redirect('/')
