from django.test import TestCase, Client

# Create your tests here.
class MapCase(TestCase):
    def test_index(self):
        c = Client()
        response = c.get("/")
        self.assertEqual(response.status_code, 200, "unexpected return code")

    def test_create_form(self):
        c = Client()
        response = c.get("/sign-up")
        self.assertEqual(response.status_code, 200, "unexpected return code")

    def test_modify_form(self):
        c = Client()
        response = c.get("/modify")
        self.assertEqual(response.status_code, 302, "unexpected return code")

    def test_connect_form(self):
        c = Client()
        response = c.get("/sign-in")
        self.assertEqual(response.status_code, 200, "unexpected return code")
