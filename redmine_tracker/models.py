# -*- coding: utf-8 -*-

import datetime

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator
from django.db import models
from redminelib.exceptions import AuthError

from .redmine import redmine_api


class User(AbstractUser):
    redmine = None

    redmine_api_key = models.CharField(max_length=255, blank=True, null=True)
    redmine_user_id = models.PositiveIntegerField(blank=True, null=True,
                                                  validators=[MaxValueValidator(999999)])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.redmine_api_key:
            self.redmine = redmine_api(self.redmine_api_key)


class Project(models.Model):
    user = models.ForeignKey(User, related_name='projects')
    name = models.CharField(max_length=255)
    project_id = models.PositiveIntegerField(validators=[MaxValueValidator(999999)])
    is_hidden = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Task(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=255)
    project = models.ForeignKey(Project)
    task_id = models.PositiveIntegerField(validators=[MaxValueValidator(999999)])
    task_name = models.CharField(max_length=255, blank=True, null=True)


class TimeEntry(models.Model):
    task = models.ForeignKey(Task, related_name='entries')
    start = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField(null=True, blank=True)


class TimeBank(models.Model):
    user = models.ForeignKey(User)
    # It's null when the project is non-billable.
    project = models.ForeignKey(Project, blank=True, null=True)
    time = models.TimeField(default=datetime.time(0, 0))
    start = models.DateTimeField(null=True, blank=True)
