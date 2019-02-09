from base64 import b64encode
from base64 import b64decode
from typing import Union


__all__ = [
    'as_bytes',
    'b64_str',
    'from_b64_str',
    'prefix_alias',
]


def as_bytes(value):
    if isinstance(value, str):
        value = value.encode('utf-8')
    return value


def b64_str(value: Union[str, bytes]) -> str:
    value = as_bytes(value)
    return b64encode(value).decode('utf-8')


def from_b64_str(value: str):
    value = value.encode('utf-8')
    return b64decode(value)


def prefix_alias(alias: str):
    if not alias.startswith('alias/'):
        alias = f'alias/{alias}'
    return alias
