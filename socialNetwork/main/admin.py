from django.contrib import admin
from .models import CustomUser, News
admin.site.register(CustomUser)
admin.site.register(News)
# Register your models here.
