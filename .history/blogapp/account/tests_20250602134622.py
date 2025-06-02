from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse


class RegisterViewTests(TestCase):
    def test_register_page_loads_correctly(self):
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "account/register.html")

    def test_successful_registration_redirects_to_login(self):
        response = self.client.post(reverse("register"), {
            "name": "Ali",
            "surname": "Yılmaz",
            "email": "ali@example.com",
            "username": "ali123",
            "password": "password123",
            "repassword": "password123"
        })
        self.assertRedirects(response, reverse("login"))
        self.assertTrue(User.objects.filter(username="ali123").exists())

    def test_registration_password_mismatch(self):
        response = self.client.post(reverse("register"), {
            "name": "Ali",
            "surname": "Yılmaz",
            "email": "ali@example.com",
            "username": "ali123",
            "password": "password123",
            "repassword": "farklıparola"
        })
        self.assertContains(response, "Parola eşleşmiyor.")

    def test_registration_username_already_exists(self):
        User.objects.create_user(username="ali123", password="password123")
        response = self.client.post(reverse("register"), {
            "name": "Ali",
            "surname": "Yılmaz",
            "email": "ali2@example.com",
            "username": "ali123",
            "password": "password123",
            "repassword": "password123"
        })
        self.assertContains(response, "Kullanıcı adı kullanılıyor.")

class LoginViewTests(TestCase):
    def test_login_page_loads_correctly(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "account/login.html")

    def test_successful_login_redirects_to_home(self):
        User.objects.create_user(username="ali123", password="password123")
        response = self.client.post(reverse("login"), {
            "username": "ali123",
            "password": "password123"
        })
        self.assertRedirects(response, reverse("home"))

    def test_login_with_wrong_credentials_shows_error(self):
        response = self.client.post(reverse("login"), {
            "username": "ali123",
            "password": "yanlıs"
        })
        self.assertContains(response, "Kullanıcı adı ya da şifre yanlış")

class LogoutViewTests(TestCase):
    def test_logout_redirects_to_home(self):
        user = User.objects.create_user(username="ali", password="password123")
        self.client.login(username="ali", password="password123")
        response = self.client.get(reverse("logout"))
        self.assertRedirects(response, reverse("home"))
