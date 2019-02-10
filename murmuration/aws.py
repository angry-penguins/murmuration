from threading import local
import boto3


cache = local()
cache.sessions = {}
cache.clients = {}


__all__ = [
    'kms_client',
    'cached_client',
    'cached_session',
]


def cached_session(region: str = None, profile: str = None):
    key = f'{region}-{profile}'
    session = cache.sessions.get(key)
    if not session:
        session = boto3.Session(region_name=region, profile_name=profile)
        cache.sessions[key] = session
    return session


def cached_client(client: str, region: str = None, profile: str = None):
    key = f'{region}-{profile}-{client}'
    client = cache.clients.get(key)
    if not client:
        session = cached_session(region, profile)
        client = cache.clients[key] = session.client('kms')
    return client


def kms_client(region: str = None, profile: str = None):
    return cached_client('kms', region, profile)
