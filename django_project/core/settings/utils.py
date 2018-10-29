# coding=utf-8

"""Helpers for settings."""
import os

# Absolute filesystem path to the Django project directory:
import urlparse

DJANGO_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    ))


def absolute_path(*args):
    """Get an absolute path for a file that is relative to the django root.

    :param args: List of path elements.
    :type args: list

    :returns: An absolute path.
    :rtype: str
    """
    return os.path.join(DJANGO_ROOT, *args)


def ensure_secret_key_file():
    """Checks that secret.py exists in settings dir.

    If not, creates one with a random generated SECRET_KEY setting."""
    secret_path = absolute_path('core', 'settings', 'secret.py')
    if not os.path.exists(secret_path):
        from django.utils.crypto import get_random_string
        secret_key = get_random_string(
            50, 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)')
        with open(secret_path, 'w') as f:
            f.write("SECRET_KEY = " + repr(secret_key) + "\n")


def ensure_unique_app_labels(installed_apps):
    """Checks that INSTALLED APPS contains unique app labels."""
    retval = ()
    for val in installed_apps:
        if val in retval:
            continue
        retval += (val, )
    return retval


def validate_url(url, end_slash=False):
    """Perform simple validation replace of provided URL.

    :param url: input url
    :type url: basestring

    :param end_slash: Set to True to end the URL with slash /
    :type end_slash: bool

    :return: the URL fix
    :rtype: basestring
    """
    # URL should not have double // after relative path

    url_splitted = urlparse.urlsplit(url)

    new_path = url_splitted.path.replace('//', '/')
    new_parse_result = (
        url_splitted.scheme,
        url_splitted.netloc,
        new_path,
        url_splitted.query,
        url_splitted.fragment
    )

    url = urlparse.urlunsplit(new_parse_result)

    # URL should not end with slash
    if url.endswith('/') and not end_slash:
        url = url[:-1]

    if not url.endswith('/') and end_slash:
        url = url + '/'

    return url


# Import the secret key
ensure_secret_key_file()
