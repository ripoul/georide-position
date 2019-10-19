from django.test import TestCase, Client

# Create your tests here.
class MapCase(TestCase):
    def test_index(self):
        c = Client()
        response = c.get("/")
        self.assertEqual(response.status_code, 200, "unexpected return code")

    def test_create_form(self):
        c = Client()
        response = c.get("/create")
        self.assertEqual(response.status_code, 200, "unexpected return code")

    def test_modifie_form(self):
        c = Client()
        response = c.get("/modifie")
        self.assertEqual(response.status_code, 302, "unexpected return code")

    def test_connect_form(self):
        c = Client()
        response = c.get("/connect")
        self.assertEqual(response.status_code, 200, "unexpected return code")