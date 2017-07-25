from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.urlresolvers import reverse_lazy


class CustomerUserCreationForm(UserCreationForm):
    url = reverse_lazy('loginsys:user_registration')
    button_text = 'Зарегистрироваться'


class CustomerAuthenticationForm(AuthenticationForm):
    url = reverse_lazy('loginsys:user_login')
    button_text = 'Войти'
