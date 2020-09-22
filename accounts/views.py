from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView

from .forms import RegistrationForm, LoginForm


class SignUpview(CreateView):
    form_class = RegistrationForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('accounts:login')


def login_page(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse('accounts:home'))
            else:
                pass
    context = {'form': form}
    return render(request, 'accounts/login.html', context)


def logout_view(request):
    logout(request)
    return redirect(reverse('accounts:login'))

@login_required
def home(request):
    return render(request, 'index.html')