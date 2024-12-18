from django33_ninja.security.apikey import APIKeyCookie, APIKeyHeader, APIKeyQuery
from django33_ninja.security.http import HttpBasicAuth, HttpBearer
from django33_ninja.security.session import SessionAuth, SessionAuthSuperUser

__all__ = [
    "APIKeyCookie",
    "APIKeyHeader",
    "APIKeyQuery",
    "HttpBasicAuth",
    "HttpBearer",
    "SessionAuth",
    "SessionAuthSuperUser",
    "django_auth",
    "django_auth_superuser",
]

django_auth = SessionAuth()
django_auth_superuser = SessionAuthSuperUser()
