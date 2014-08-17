from django.contrib import admin
from django.contrib.auth.models import User
from users.models import Punctuation,UserExtra

# Register your models here.
admin.site.register(Punctuation)
admin.site.register(UserExtra)