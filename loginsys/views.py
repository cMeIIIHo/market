from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login

# Create your views here.


def registration(request):
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
    template = 'loginsys/registration.html'
    context = {'form': form}
    return render(request, template, context)





