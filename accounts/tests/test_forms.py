from django.test import TestCase

from accounts.forms import UserAdminCreationForm, UserAdminChangeForm, LoginForm, RegistrationForm


class TestUserAdminCreationForm(TestCase):
    def test_with_valid_data(self):
        data = {'email': 'testuser@gmail.com', 'password1': 'password1', 'password2': 'password1'}
        form = UserAdminCreationForm(data)
        self.assertTrue(form.is_valid())

    def test_with_unmatching_passwords(self):
        data = {'email': 'testuser@gmail.com', 'password1': 'password1', 'password2': 'password2'}
        form = UserAdminCreationForm(data)
        self.assertFalse(form.is_valid())

    def test_with_no_email(self):
        data = {'email': '', 'password1': 'password1', 'password2': 'password2'}
        form = UserAdminCreationForm(data)
        self.assertFalse(form.is_valid())


class TestUserAdminChangeForm(TestCase):
    def test_with_vailid_data(self):
        data = {'email': 'testuser@gmail.com', 'password': 'password3', 'is_active': False, 'admin': False}
        form = UserAdminChangeForm(data, initial={'password': 'password1'})
        self.assertTrue(form.is_valid())

    def test_with_no_email(self):
        data = {'email': '', 'password': 'password3', 'is_active': False, 'admin': False}
        form = UserAdminChangeForm(data, initial={'password': 'password1'})
        self.assertFalse(form.is_valid())


class TestLoginForm(TestCase):
    def test_with_valid_data(self):
        data = {'email': 'testuser@gmail.com', 'password': 'password3'}
        form = LoginForm(data)
        self.assertTrue(form.is_valid())

    def test_with_no_email(self):
        data = {'email': '', 'password': 'password3'}
        form = LoginForm(data)
        self.assertFalse(form.is_valid())

    def test_with_no_password(self):
        data = {'email': 'testuser@gmail.com', 'password': ''}
        form = LoginForm(data)
        self.assertFalse(form.is_valid())


class TestRegistrationForm(TestCase):
    def test_with_valid_data(self):
        data = {'email': 'testuser@gmail.com', 'password1': 'password1', 'password2': 'password1'}
        form = RegistrationForm(data)
        self.assertTrue(form.is_valid())

    def test_with_unmatching_passwords(self):
        data = {'email': 'testuser@gmail.com', 'password1': 'password1', 'password2': 'password2'}
        form = RegistrationForm(data)
        self.assertFalse(form.is_valid())

    def test_with_no_email(self):
        data = {'email': '', 'password1': 'password1', 'password2': 'password2'}
        form = RegistrationForm(data)
        self.assertFalse(form.is_valid())

