from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.core import mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from accounts.forms import RegistrationForm, LoginForm
from accounts.token import account_activation_token


class TestSignupView(TestCase):
    def setUp(self):
        self.url = reverse('accounts:signup')
        self.User = get_user_model()

    def test_unauthenticated_user(self):
        user = self.User.objects.create(email='testemail@gmail.com', password='password1')
        self.client._login(user)
        response = self.client.get(self.url)
        expected_url = reverse('accounts:home')     # change expected_url in your project
        self.assertRedirects(response, expected_url, 302)

    def test_template_used(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'accounts/signup.html')

    def test_response_status_code(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)

    def test_post_method_with_valid_data(self):
        data = {'email': 'testuser@gmail.com', 'password1': 'password1', 'password2': 'password1'}
        response = self.client.post(self.url, data, follow=True)
        user = response.context['user']
        uid = urlsafe_base64_encode(force_bytes(user.id))
        token = account_activation_token.make_token(user)

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Activate your account')
        self.assertEqual(mail.outbox[0].from_email, '<youremail>')      # change to your email <youremail>
        self.assertEqual(mail.outbox[0].to, ['testuser@gmail.com']) # self.user.email
        self.assertEqual(mail.outbox[0].body, "\nHi ,\nPlease click on the link to confirm your registration,\n"
                                   "http://testserver/accounts/activate/" + str(uid) + "/" + str(token) + "/\n"
                         )

        message = list(response.context.get('messages'))[0]
        self.assertEquals(message.tags, 'success')
        self.assertEquals(message.message, 'We have sent you an activation link in your email. Please confirm '
                                           'your email to continue')

    def test_post_method_with_invalid_data(self):
        data = {'email': 'testuser@gmail.com', 'password1': 'password1', 'password2': 'password22'} # passwords dont match
        response = self.client.post(self.url, data, follow=True)
        message = list(response.context.get('messages'))[0]
        self.assertEquals(message.tags, 'error')
        self.assertEquals(message.message, 'Passwords do not match')

    def test_context_items(self):
        response = self.client.get(self.url)
        self.assertTrue('form' in response.context)

    def test_form(self):
        response = self.client.get(self.url)
        form = response.context['form']
        self.assertIsInstance(form, RegistrationForm)

    def test_csrf_token(self):
        response = self.client.get(self.url)
        self.assertContains(response, 'csrfmiddlewaretoken')


class TestActivateAccountView(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.user = self.User.objects.create(email='testuser@gmail.com', password='password1', is_active=False)

    def test_test_with_valid_token(self):
        uidb64 = urlsafe_base64_encode(force_bytes(self.user.id))
        token = account_activation_token.make_token(self.user)

        url = reverse('accounts:activate', args=[uidb64, token])

        response = self.client.get(url, follow=True)
        message = list(response.context.get('messages'))[0]
        self.assertRedirects(response, reverse('accounts:login'), 302)
        self.assertEquals(message.tags, 'success')
        self.assertEquals(message.message, 'Thank you for confirming your email. You can now login.')

        user = self.User.objects.get(id=1)

        self.assertTrue(user.is_active)     # user status updated to active

    def test_with_invalid_token(self):
        uidb64 = urlsafe_base64_encode(force_bytes(3))  # user with id = 3 DoesNotExist
        token = account_activation_token.make_token(self.user)
        url = reverse('accounts:activate', args=[uidb64, token])

        response = self.client.get(url, follow=True)
        message = list(response.context.get('messages'))[0]
        self.assertRedirects(response, reverse('accounts:login'), 302)
        self.assertEquals(message.tags, 'error')
        self.assertEquals(message.message, 'Activation link is invalid!')


class TestLoginView(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.user = self.User.objects.create_user(email='testemail@gmail.com', password='password1')

        self.url = reverse('accounts:login')

    def test_unauthenticated_user(self):
        self.client._login(self.user)
        response = self.client.get(self.url)
        expected_url = reverse('accounts:home')  # change expected_url in your project
        self.assertRedirects(response, expected_url, 302)

    def test_template_used(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_response_status_code(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)

    def test_post_method_with_valid_credentials(self):
        data = {'email': 'testemail@gmail.com', 'password': 'password1'}    # user with these credentials exists
        response = self.client.post(path=self.url, data=data, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)

    def test_with_invalid_credentials(self):
        data = {'email': 'testemail2@gmail.com', 'password': 'password2'}    # user with these credentials doesn't exist
        response = self.client.post(self.url, data, follow=True)
        message = list(response.context.get('messages'))[0]
        self.assertEquals(message.tags, 'error')
        self.assertEquals(message.message, 'Incorrect email or password')

    def test_context_items(self):
        response = self.client.get(self.url)
        self.assertTrue('form' in response.context)

    def test_form(self):
        response = self.client.get(self.url)
        form = response.context['form']
        self.assertIsInstance(form, LoginForm)

    def test_csrf_token(self):
        response = self.client.get(self.url)
        self.assertContains(response, 'csrfmiddlewaretoken')


class TestLogoutView(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.user = self.User.objects.create(email='testemail@gmail.com', password='password1')
        self.url = reverse('accounts:logout')

    def test_logout(self):
        self.client._login(self.user)
        response = self.client.get(self.url)
        expected_url = reverse('accounts:login')
        self.assertRedirects(response, expected_url, 302)

        user = self.User.objects.get(id=1)
        self.assertNotIn(user.id, self.client.session)  # user does not have an active session i.e. is logged out
