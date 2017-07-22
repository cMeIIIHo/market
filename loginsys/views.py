from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse

# Create your views here.


def user_registration(request):

    # redirect_url tries to take value from POST dictionary, if not - it uses url where user came from.
    redirect_url = request.POST.get('redirect_url', request.META['HTTP_REFERER'])
    if request.method == 'POST':
        filled_form = UserCreationForm(request.POST)
        if filled_form.is_valid():
            filled_form.save()
            new_user = authenticate(username=filled_form.cleaned_data['username'],
                                    password=filled_form.cleaned_data['password1'])
            login(request, new_user)
            return redirect(redirect_url)
        else:
            form = filled_form
    else:
        form = UserCreationForm()
    form.url = reverse('loginsys:user_registration')
    form.button_text = 'Зарегистрироваться'
    template = 'loginsys/user_registration.html'
    context = {'form': form, 'redirect_url': redirect_url}
    return render(request, template, context)


def user_login(request):

    redirect_url = request.POST.get('redirect_url', request.META['HTTP_REFERER'])
    if request.method == 'POST':
        filled_form = AuthenticationForm(request, request.POST)
        if filled_form.is_valid():
            user = authenticate(username=filled_form.cleaned_data['username'],
                                password=filled_form.cleaned_data['password'])
            login(request, user)
            return redirect(redirect_url)
        else:
            form = filled_form
    else:
        form = AuthenticationForm(request)
    form.url = reverse('loginsys:user_login')
    form.button_text = 'Войти'
    template = 'loginsys/user_login.html'
    context = {'form': form, 'redirect_url': redirect_url}
    return render(request, template, context)


def user_logout(request):
    logout(request)
    return redirect('/')
