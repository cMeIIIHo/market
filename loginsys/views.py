from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from loginsys.forms import CustomerAuthenticationForm, CustomerUserCreationForm
from market.settings import INSTALLED_APPS
from django.core.urlresolvers import reverse


def user_registration(request):

    # redirect_url tries to take value from POST dictionary, if not - it uses url where user came from.
    redirect_url = request.POST.get('redirect_url', request.META.get('HTTP_REFERER', reverse('catalog:index')))
    if request.method == 'POST':
        filled_form = CustomerUserCreationForm(request.POST)
        if filled_form.is_valid():
            filled_form.save()
            new_user = authenticate(username=filled_form.cleaned_data['username'],
                                    password=filled_form.cleaned_data['password1'])
            login(request, new_user)
            if 'ordersys' in INSTALLED_APPS:
                from ordersys.models import Order
                Order.synchronize(new_user, request.session)
            return redirect(redirect_url)
        else:
            form = filled_form
    elif request.user.is_authenticated():
        return redirect(redirect_url)
    else:
        form = CustomerUserCreationForm()
    template = 'loginsys/user_registration.html'
    context = {'form': form, 'redirect_url': redirect_url}
    return render(request, template, context)


def user_login(request):

    redirect_url = request.POST.get('redirect_url', request.META.get('HTTP_REFERER', reverse('catalog:index')))
    if request.method == 'POST':
        filled_form = CustomerAuthenticationForm(request, request.POST)
        if filled_form.is_valid():
            user = authenticate(username=filled_form.cleaned_data['username'],
                                password=filled_form.cleaned_data['password'])
            login(request, user)
            if 'ordersys' in INSTALLED_APPS:
                from ordersys.models import Order
                Order.synchronize(user, request.session)
            return redirect(redirect_url)
        else:
            form = filled_form
    elif request.user.is_authenticated():
        return redirect(redirect_url)
    else:
        form = CustomerAuthenticationForm(request)
    template = 'loginsys/user_login.html'
    context = {'form': form, 'redirect_url': redirect_url}
    return render(request, template, context)


def user_logout(request):

    logout(request)
    return redirect('/')
