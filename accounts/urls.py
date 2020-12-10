from django.urls import path
from django.contrib.auth import views as auth_views

from .views import signup_page, login_page, home, logout_view, activate_account_page

app_name = 'accounts'
urlpatterns = [
    path('accounts/signup/', signup_page, name='signup'),
    path('accounts/activate/<slug:uidb64>/<slug:token>/', activate_account_page, name='activate'),
    path('accounts/login/', login_page, name='login'),
    path('accounts/logout/', logout_view, name='logout'),


    # Reset Passoword Urls
    path('accounts/reset-password', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'),
         name='reset_password'),
    path('accounts/password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_sent.html'),
         name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_form.html'),
         name='password_reset_confirm'),
    path('accounts/reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_done.html'),
         name='password_reset_complete'),

    path('', home, name='home'),
]


# To update password reset functionality