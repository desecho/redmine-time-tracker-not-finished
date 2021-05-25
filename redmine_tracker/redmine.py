from django.conf import settings
from redminelib import Redmine


def redmine_api(key):
    return Redmine(settings.REDMINE_URL, key=key)
