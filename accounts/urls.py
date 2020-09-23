from django.urls import path
from .views import signup_page, login_page, home, logout_view, activate_account_page

app_name = 'accounts'
urlpatterns = [
    path('accounts/signup/', signup_page, name='signup'),
    path('accounts/activate/<slug:uidb64>/<slug:token>/', activate_account_page, name='activate'),
    path('accounts/login/', login_page, name='login'),
    path('accounts/logout/', logout_view, name='logout'),
    path('', home, name='home'),
]