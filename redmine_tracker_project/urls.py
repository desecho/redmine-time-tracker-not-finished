"""redmine_tracker_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.views import login

from redmine_tracker.views.tracker import HomeView
from redmine_tracker.views.user import (
    PreferencesView, logout_view, ImportProjectsView, ToggleProjectView,
)

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),

    # User
    url(r'^login/$', login, {'template_name': 'user/login.html'}, name='login'),
    url(r'^logout/$', logout_view, name='logout'),

    url(r'^preferences/$', PreferencesView.as_view(), name='preferences'),
    url(r'^import-projects/$', ImportProjectsView.as_view(), name='import_projects'),
    url(r'^toggle-project/$', ToggleProjectView.as_view(), name='toggle_project'),

    url(r'^admin/', admin.site.urls),
]
