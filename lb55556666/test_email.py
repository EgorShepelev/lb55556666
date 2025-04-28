import unittest
from myform import my_form

class TestEmailValidation(unittest.TestCase):
    def test_valid_emails(self):
        """Проверка валидных email"""
        valid_emails = [
            "user@example.com",
            "alice.bob@example.org",
            "john.doe+label@example.co.uk",
            "firstname-lastname@example.com",
            "email@subdomain.example.com",
            "123456@example.com",
            "_______@example.com",
            "email@example.name"
        ]
        
        for email in valid_emails:
            with self.subTest(email=email):
                self.assertTrue(validate_email(email), f"Email {email} должен быть валидным")

    def test_invalid_emails(self):
        """Проверка невалидных email"""
        invalid_emails = [
            "",                     # пустая строка
            "plaintext",            # нет @
            "@missingusername.com", # нет имени
            "user@.com",            # точка после @
            "user@example..com",    # две точки подряд
            "user@example.com.",    # точка в конце
            "user name@example.com", # пробел в имени
            "user@-example.com",    # дефис в начале домена
            "user@example_.com",    # подчеркивание в домене
            "user@.hidden.com"      # точка в начале домена
        ]
        
        for email in invalid_emails:
            with self.subTest(email=email):
                self.assertFalse(validate_email(email), f"Email {email} должен быть невалидным")

if __name__ == '__main__':
    unittest.main()