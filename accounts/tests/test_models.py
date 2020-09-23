from django.contrib.auth import get_user_model
from django.test import TestCase


class TestModelManager(TestCase):
    def setUp(self):
        self.email = 'user@gmail.com'
        self.password1 = 'password1'
        self.password2 = 'password1'
        self.User = get_user_model()

    def test_createuser_method(self):
        user = self.User.objects.create_user(email=self.email, password=self.password1)
        self.assertEquals(user.is_active, True)
        self.assertEquals(user.is_staff, False)
        self.assertEquals(user.is_admin, False)
        self.assertEquals(self.User.objects.get(id=1), user)

    def test_createstaff_method(self):
        user = self.User.objects.create_staffuser(email=self.email, password=self.password1)
        self.assertEquals(user.is_active, True)
        self.assertEquals(user.is_staff, True)
        self.assertEquals(user.is_admin, False)
        self.assertEquals(self.User.objects.get(id=1), user)

    def test_createsuperuser_method(self):
        user = self.User.objects.create_superuser(email=self.email, password=self.password1)
        self.assertEquals(user.is_active, True)
        self.assertEquals(user.is_staff, True)
        self.assertEquals(user.is_admin, True)
        self.assertEquals(self.User.objects.get(id=1), user)
        self.assertEquals(user.is_admin, True)


