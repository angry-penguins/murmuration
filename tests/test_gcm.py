from unittest import TestCase
import pytest
from murmuration.gcm import encrypt
from murmuration.gcm import decrypt
from murmuration import settings


__all__ = [
    'Gcm',
]


class Gcm(TestCase):
    encryption_key = 'test key'
    plaintext = 'the quick brown fox'
    header = 'header'

    def test_encrypt(self):
        cipher_text = encrypt(self.plaintext, self.encryption_key, self.header)
        result = decrypt(cipher_text, self.encryption_key)
        self.assertEqual(self.plaintext, result)

    def test_default_key(self):
        old_encryption_key = settings.encryption_key
        settings.encryption_key = self.encryption_key
        cipher_text = encrypt(self.plaintext, auth_header=self.header)
        result = decrypt(cipher_text)
        settings.encryption_key = old_encryption_key
        self.assertEqual(self.plaintext, result)

    def test_null_decryption(self):
        with pytest.raises(ValueError) as ex:
            decrypt(self.plaintext, self.encryption_key)
        self.assertEqual(
            'Unpacked value did not have exactly five pieces',
            ex.value.args[0])
