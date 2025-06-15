import unittest
from core import crypto_utils

class TestCryptoUtils(unittest.TestCase):
    def setUp(self):
        self.password = 'testpassword123'
        self.data = 'Sensitive information!'

    def test_encrypt_decrypt(self):
        encrypted = crypto_utils.encrypt(self.data, self.password)
        self.assertIsInstance(encrypted, str)
        decrypted = crypto_utils.decrypt(encrypted, self.password)
        self.assertEqual(decrypted, self.data)

    def test_decrypt_with_wrong_password(self):
        encrypted = crypto_utils.encrypt(self.data, self.password)
        with self.assertRaises(Exception):
            crypto_utils.decrypt(encrypted, 'wrongpassword')

if __name__ == '__main__':
    unittest.main()
