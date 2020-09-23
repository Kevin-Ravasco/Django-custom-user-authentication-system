from django.test import SimpleTestCase
from django.urls import reverse, resolve

from accounts.views import signup_page, login_page,  logout_view, activate_account_page


class TestUrls(SimpleTestCase):
    def test_signup_url(self):
        url = reverse('accounts:signup')
        resolved = resolve(url)
        self.assertEqual(resolved.func, signup_page)
        self.assertEqual(resolved.namespace, 'accounts')
        self.assertEqual(url, '/accounts/signup/')

    def test_login_url(self):
        url = reverse('accounts:login')
        resolved = resolve(url)
        self.assertEqual(resolved.func, login_page)
        self.assertEqual(resolved.namespace, 'accounts')
        self.assertEqual(url, '/accounts/login/')

    def test_activate_url(self):
        url = reverse('accounts:activate', args=['uid', 'token'])
        resolved = resolve(url)
        self.assertEqual(resolved.func, activate_account_page)
        self.assertEqual(resolved.namespace, 'accounts')
        self.assertEqual(url, '/accounts/activate/uid/token/')

    def test_logout_url(self):
        url = reverse('accounts:logout')
        resolved = resolve(url)
        self.assertEqual(resolved.func, logout_view)
        self.assertEqual(resolved.namespace, 'accounts')
        self.assertEqual(url, '/accounts/logout/')
