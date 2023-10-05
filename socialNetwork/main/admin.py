from django.contrib import admin
from .models import Friendship, Photos, CustomUser, News, Notifications, Feed
admin.site.register(CustomUser)
admin.site.register(News)
admin.site.register(Friendship)
admin.site.register(Photos)
admin.site.register(Notifications)
admin.site.register(Feed)
# Register your models here.
