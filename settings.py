import os

SECRET_KEY = None
APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))

DEBUG = False
DEBUG_TB_ENABLED = False
DEBUG_TB_INTERCEPT_REDIRECTS = False

SQLALCHEMY_DATABASE_URI = None
SQLALCHEMY_TRACK_MODIFICATIONS = False

FAKE_DATA_POINTS = 100
LOCATION_BOUNDS_LAT_MIN = 47.386
LOCATION_BOUNDS_LAT_MAX = 47.393
LOCATION_BOUNDS_LON_MIN = 8.505
LOCATION_BOUNDS_LON_MAX = 8.525

try:
    from local_settings import *
except ImportError:
    pass
