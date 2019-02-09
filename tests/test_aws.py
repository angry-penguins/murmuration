import os
from subprocess import Popen
from unittest import TestCase
from murmuration.aws import cached_session
from murmuration.aws import kms_client


__all__ = [
    'Aws',
]


class Aws(TestCase):
    def setUp(self):
        region = os.environ.get('AWS_REGION', 'us-east-2')
        access_key_id = os.environ.get('AWS_ACCESS_KEY_ID', 'cody')
        secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY', 'jinx')
        handle = Popen([
            '/bin/bash',
            '-c',
            f'source bin/activate '
            f'  && aws --profile=company configure set region {region}'
            f'  && aws --profile=company configure '
            f'set aws_access_key_id {access_key_id}'
            f'  && aws --profile=company configure set '
            f'aws_secret_access_key {secret_access_key}' ])
        handle.communicate()

    def test_session(self):
        session = cached_session('us-east-2', 'company')
        self.assertEqual(session.profile_name, 'company')
        self.assertEqual(session.region_name, 'us-east-2')
        x = cached_session('us-east-2', 'company')
        self.assertIs(session, x)

        client = kms_client()
        self.assertEqual(client.__class__.__name__, 'KMS')
