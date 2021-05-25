# -*- coding: utf-8 -*-


from django.contrib import admin

from .models import User, Project, Task, TimeEntry, TimeBank

admin.site.register(User)
admin.site.register(Project)
admin.site.register(Task)
admin.site.register(TimeEntry)
admin.site.register(TimeBank)
