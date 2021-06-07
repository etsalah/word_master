"""Module to hold configuration classes for the application"""
import os
from datetime import timedelta
from dotenv import load_dotenv, find_dotenv
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


load_dotenv(find_dotenv(), override=True)


def default_sqlite_file_path():
    """This is a function to return a default file to use as an sqlite db file
    if none is provided"""
    return 'sqlite:///{0}'.format(os.path.join(BASE_DIR, 'app.db'))


class Config:  # pylint: disable=too-few-public-methods
    """This is class serves as a configuration container for the project"""
    SECRET_KEY = os.environ.get(
        'SECRET_KEY') or "NOT_SET_9sjdfksdfkjsdkfjsdkf"
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL') or default_sqlite_file_path()
    SECURITY_PASSWORD_SALT = os.environ.get(
        'SECURITY_PASSWORD_SALT', 'DummmypASSWORLDsalT')
    ROOT_USER_EMAIL = os.environ.get('ROOT_USER_EMAIL', 'admin@example.com')
    ROOT_USER_USERNAME = os.environ.get('ROOT_USER_USERNAME', 'admin')
    ROOT_USER_PASSWORD = os.environ.get('ROOT_USER_PASSWORD', '')
    ROOT_USER_NAME = os.environ.get('ROOT_USER_NAME', 'admin')

    permanent_session_lifetime = os.environ.get('PERMANENT_SESSION_LIFETIME')
    if permanent_session_lifetime:
        permanent_session_lifetime = int(permanent_session_lifetime)
    else:
        permanent_session_lifetime = timedelta(days=31)

    PERMANENT_SESSION_LIFETIME = permanent_session_lifetime
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEFAULT_ROW_COUNT = os.environ.get('DEFAULT_ROW_COUNT', 20)
