import os
from subprocess import Popen
from unittest import TestCase
from murmuration.aws import cached_session
from murmuration.aws import cached_client
from murmuration.helpers import b64_str


__all__ = [
    'Aws',
]


class Aws(TestCase):
    plaintext = 'hello, peanut!'
    profile = 'test'

    def setUp(self):
        region = os.environ.get('AWS_REGION')
        access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
        secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
        values = [
            ('region', region),
            ('aws_access_key_id', access_key_id),
            ('aws_secret_access_key', secret_access_key),
        ]
        for key, value in values:
            if not value:
                continue
            handle = Popen([
                '/bin/bash',
                '-c',
                f'source bin/activate '
                f'  && aws --profile={self.profile} '
                f'configure set {key} {value}',
            ])
            handle.communicate()

    def kms(self):
        from murmuration.kms import encrypt
        from murmuration.kms import decrypt
        value = encrypt(self.plaintext, 'dev', profile=self.profile)
        value = decrypt(value, profile=self.profile)
        self.assertEqual(value, self.plaintext)

    def kms_wrapped(self):
        from murmuration.kms_wrapped import encrypt
        from murmuration.kms_wrapped import decrypt
        value = encrypt(self.plaintext, 'dev', profile=self.profile)
        value = decrypt(value, profile=self.profile)
        self.assertEqual(value, self.plaintext)
        with self.assertRaises(ValueError):
            decrypt('nonce')
        with self.assertRaises(ValueError):
            decrypt('no|nce')
        with self.assertRaises(ValueError):
            decrypt(f'{b64_str("no")}|nce')

    def test_session(self):
        session = cached_session(region='us-east-2', profile=self.profile)
        self.assertEqual(session.profile_name, self.profile)
        self.assertEqual(session.region_name, 'us-east-2')
        x = cached_session(region='us-east-2', profile=self.profile)
        self.assertIs(session, x)
        self.kms()
        self.kms_wrapped()

    def test_cached_client(self):
        x = cached_client('ec2', region='us-east-2', profile=self.profile)
        self.assertEqual(x.__class__.__name__.lower(), 'ec2')
