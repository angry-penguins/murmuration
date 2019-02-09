from .helpers import as_bytes
from .helpers import from_b64_str
from .aws import kms_client
from .helpers import prefix_alias
from .gcm import encrypt_bytes as gcm_encrypt
from .gcm import decrypt_bytes as gcm_decrypt


def encrypt_bytes(
        plain_text: bytes,
        alias: str,
        region: str = None,
        profile: str = None) -> str:
    client = kms_client(region, profile)
    alias = prefix_alias(alias)
    response = client.generate_data_key(KeyId=alias, KeySpec='AES_256')
    data_key = response['Plaintext']
    header = response['CiphertextBlob']
    value = gcm_encrypt(plain_text, data_key, auth_header=header)
    return value


def decrypt_bytes(
        packed_value: str,
        region: str = None,
        profile: str = None) -> bytes:
    pieces = packed_value.split('|', 1)
    wrapped_data_key = pieces[0]
    wrapped_data_key = from_b64_str(wrapped_data_key)
    client = kms_client(region, profile)
    response = client.decrypt(CiphertextBlob=wrapped_data_key)
    data_key = response['Plaintext']
    plain_text = gcm_decrypt(packed_value, data_key)
    return plain_text


def encrypt(plain_text, alias, region: str = None, profile: str = None) -> str:
    plain_text = as_bytes(plain_text)
    data = encrypt_bytes(plain_text, alias, region, profile)
    return data


def decrypt(packed_value: str, region: str = None, profile: str = None):
    data = decrypt_bytes(packed_value, region, profile)
    return data.decode('utf-8')
