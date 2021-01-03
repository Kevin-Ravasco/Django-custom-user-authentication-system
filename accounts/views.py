from smtplib import SMTPException
from socket import gaierror

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .forms import RegistrationForm, LoginForm
from .token import account_activation_token
from .decorators import unauthenticated_user


@unauthenticated_user
def signup_page(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            to_email = form.cleaned_data.get('email')
            current_site = get_current_site(request)
            mail_subject = 'Activate your account'
            message = render_to_string('accounts/email_verification.html', {'user': user, 'domain': current_site.domain,
                                                                            'uid': urlsafe_base64_encode(
                                                                                force_bytes(user.id)),
                                                                            'token': account_activation_token.make_token(
                                                                                user)})
            try:
                send_mail(mail_subject, message, '<youremail>', [to_email])
                messages.success(request, 'We have sent you an activation link in your email. Please confirm your'
                                          ' email to continue')
            except (ConnectionAbortedError, SMTPException, gaierror):
                messages.error(request, 'An error occurred. Please ensure you have good internet connection and you have entered a valid email address')
                user.delete()
        else:
            if form.errors:
                for field in form:
                    for error in field.errors:
                        messages.error(request, error)
            form = RegistrationForm()

    context = {
        'form': form
    }
    return render(request, 'accounts/signup.html', context)


def activate_account_page(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Thank you for confirming your email. You can now login.')
        return redirect(settings.LOGIN_URL)
    else:
        messages.error(request, 'Activation link is invalid!')
        return redirect(settings.LOGIN_URL)


@unauthenticated_user
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
                return redirect(settings.LOGIN_REDIRECT_URL)  # change expected_url in your project
            else:
                messages.error(request, 'Incorrect email or password')
        else:
            if form.errors:
                for field in form:
                    for error in field.errors:
                        messages.error(request, error)

    context = {'form': form}
    return render(request, 'accounts/login.html', context)


def logout_view(request):
    logout(request)
    return redirect(settings.LOGOUT_REDIRECT_URL)


""" 
    This is a dummy login view
    remove it from this app and use your own homeview
"""
@login_required
def home(request):
    return render(request, 'index.html')
