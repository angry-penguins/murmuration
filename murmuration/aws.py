from threading import local
import boto3


cache = local()


__all__ = [
    'kms_client',
    'cached_client',
    'cached_session',
    'threadlocal_var',
]


def threadlocal_var(varname, factory, *a, **k):
    v = getattr(cache, varname, None)
    if v is None:
        v = factory(*a, **k)
        setattr(cache, varname, v)
    return v


def cached_session(region: str = None, profile: str = None):
    key = f'{region}-{profile}'
    sessions = threadlocal_var('session', dict)
    session = sessions.get(key)
    if not session:
        session = boto3.Session(region_name=region, profile_name=profile)
        sessions[key] = session
    return session


def cached_client(client: str, region: str = None, profile: str = None):
    key = f'{region}-{profile}-{client}'
    clients = threadlocal_var('client', dict)
    x = clients.get(key)
    if not x:
        session = cached_session(region, profile)
        x = clients[key] = session.client(client)
    return x


def kms_client(region: str = None, profile: str = None):
    return cached_client('kms', region, profile)
