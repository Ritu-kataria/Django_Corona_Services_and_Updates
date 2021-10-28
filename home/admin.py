from django.contrib import admin
from home.models import Feedback
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


admin.site.register(Feedback)
