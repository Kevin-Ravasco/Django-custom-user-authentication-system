from django.urls import path
from .views import SignUpview, login_page, home, logout_view

app_name = 'accounts'
urlpatterns = [
    path('accounts/signup/', SignUpview.as_view(), name='signup'),
    path('accounts/login/', login_page, name='login'),
    path('accounts/logout/', logout_view, name='logout'),
    path('', home, name='home'),
]