from django.contrib import admin
from .models import Friendship, Photos, CustomUser, News
admin.site.register(CustomUser)
admin.site.register(News)
admin.site.register(Friendship)
admin.site.register(Photos)
# Register your models here.
