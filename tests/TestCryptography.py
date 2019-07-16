import unittest
import app.utils as utils

class TestCryptography(unittest.TestCase):
    def test_encrypt_decrypt(self):
        textToEncypt = "some random text"
        encryptedText = utils.encrypt(textToEncypt, 'some_password')
        decryted_text = utils.decrypt(encryptedText, 'some_password')
        self.assertEqual(textToEncypt, decryted_text)

    def test_double_secure(self):
        textToEncypt = "this is a double secure test"
        encryptedText = utils.encrypt(textToEncypt, 'some_password', True)
        decryted_text = utils.decrypt(encryptedText, 'some_password', True)
        self.assertEqual(textToEncypt, decryted_text)

    def test_negative_decryption(self):
        textToEncypt = "some random text"
        encryptedText = utils.encrypt("Some Random Text", 'some_password')
        decryted_text = utils.decrypt(encryptedText, 'some_password')
        self.assertNotEqual(textToEncypt, decryted_text)

    def test_random_salt(self):
        textToEncrypt = "test random salt"
        encrypted_text1 = utils.encrypt(textToEncrypt, 'some_password')
        encrypted_text2 = utils.encrypt(textToEncrypt, 'some_password')
        self.assertNotEqual(encrypted_text1, encrypted_text2)

