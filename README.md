# murmuration ![Build Status](https://codebuild.us-east-2.amazonaws.com/badges?uuid=eyJlbmNyeXB0ZWREYXRhIjoiWk1NT3pKUUVNRXJ1THFrd2ZncTBRRlVWNGl5Nmk3czJKU21ldEpOMmJHV0NRYjBoK2lESUFuWnAyS3FtMUQwakU1bW95MXlsYW9SZy9KakxER1RsemNVPSIsIml2UGFyYW1ldGVyU3BlYyI6InVJdlBpMnBMYTBRNHhQa0siLCJtYXRlcmlhbFNldFNlcmlhbCI6MX0%3D&branch=master)
encryption primitives for use with aws kms

## aes + galois counter mode encryption

```python
from murmuration import gcm
key = 'this is my secret encryptuion key'
plaintext = 'the quick brown fox jumps over the lazy dog'
ciphertext = gcm.encrypt(plaintext, key, 'header')
decrypted = gcm.decrypt(ciphertext, key)
assert decrypted == plaintext
```

## encryption using kms (for use with aws)

You can also use kms as an encryption / decryption service.  This does
incur kms costs and require kms setup.  The `region` and `profile` parameters
do not have to be specified.  If they are not specified, the values will
be inferred [in the order specified by boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html#configuring-credentials):


>  1. Passing credentials as parameters in the `boto.client()` method
>  2. Passing credentials as parameters when creating a `Session` object
>  3. Environment variables
>  4. Shared credential file (`~/.aws/credentials`)
>  5. AWS config file (`~/.aws/config`)
>  6. Assume Role provider
>  7. Boto2 config file (`/etc/boto.cfg` and `~/.boto`)
>  8. Instance metadata service on an Amazon EC2 instance 
>     that has an IAM role configured.

```python
from murmuration import kms
plaintext = 'the quick brown fox jumps over the lazy dog'
key_alias = 'my kms key alias'
ciphertext = kms.encrypt(plaintext, key_alias, region='us-west-1', profile='company')
decrypted = kms.decrypt(ciphertext, region='us-west-1', profile='company')
assert decrypted == plaintext
```

## wrapped encryption using kms (for use with aws)

You can also use wrapped kms data keys for encryption to protect the underlying
kms key.  Using this does functionality will incur kms costs and require kms 
setup.  The `region` and `profile` parameters do not have to be specified.  
If they are not specified, the values will
be inferred [in the order specified by boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html#configuring-credentials):


>  1. Passing credentials as parameters in the `boto.client()` method
>  2. Passing credentials as parameters when creating a `Session` object
>  3. Environment variables
>  4. Shared credential file (`~/.aws/credentials`)
>  5. AWS config file (`~/.aws/config`)
>  6. Assume Role provider
>  7. Boto2 config file (`/etc/boto.cfg` and `~/.boto`)
>  8. Instance metadata service on an Amazon EC2 instance 
>     that has an IAM role configured.

```python
from murmuration import kms_wrapped
plaintext = 'the quick brown fox jumps over the lazy dog'
key_alias = 'my kms key alias'
ciphertext = kms_wrapped.encrypt(plaintext, key_alias, region='us-west-1', profile='company')
decrypted = kms_wrapped.decrypt(ciphertext, region='us-west-1', profile='company')
assert decrypted == plaintext
```
