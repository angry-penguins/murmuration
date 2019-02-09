from threading import local
import boto3


cache = local()
cache.sessions = {}


__all__ = [
    'kms_client',
]


def cached_session(region: str = None, profile: str = None):
    key = f'{region}-{profile}'
    session = cache.sessions.get(key)
    if not session:
        session = boto3.Session(region_name=region, profile_name=profile)
        cache.sessions[key] = session
    return session


def kms_client(region: str = None, profile: str = None):
    session = cached_session(region, profile)
    client = session.client('kms')
    return client
