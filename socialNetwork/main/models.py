from django.db import models
from django.contrib.auth.models import AbstractUser,Group,Permission

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    about = models.CharField(max_length=150, blank=True)
    birthday = models.DateField(blank=True, null=True)
    residence = models.CharField(max_length=20, blank=True)
    groups = models.ManyToManyField(Group, related_name='custom_user_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_set', blank=True)
    avatar = models.ImageField(upload_to='main/avatars/', null=True, blank=True, default='main/avatars/default-avatar.png')
    # для работы с медиа добавляем media в settings и теперь в html шаблонах доступны пути

class News(models.Model):
    user = models.ForeignKey(CustomUser(), on_delete=models.CASCADE, related_name='news') #если создаем с помощью один к одному, то пользователь будет уникальным и макс 1 новость
    news = models.TextField(blank=True)
    time_created = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    user_liked = models.ManyToManyField(CustomUser, blank=True, related_name='liked_news')

    def __str__(self):
        return self.user.username

class Friendship(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='friends')
    friend = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('user', 'friend')

    def __str__(self):
        return self.user.username

class Photos(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='photos')
    photos = models.URLField()
    def __str__(self):
        return self.user.username