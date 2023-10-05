from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import UserChangeForm, UserNewsForm, UserAvatarForm
from .models import News, CustomUser, Friendship, Photos, Notifications, Feed
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django_registration.signals import user_registered, user_activated
from django.contrib.auth import get_user_model
from django.views import View
from django.utils.decorators import method_decorator
from bs4 import BeautifulSoup
import requests
def index(request):
    return redirect('profile')

def pw_reset_done(request):
    return render(request, 'django_registration/password_reset_done.html')
def reset_is_done(request):
    return render(request, 'django_registration/password_reset_is_done.html')

def redirect_profile(request):
    return redirect('profile')

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        user = request.user
        form = UserChangeForm(instance=user)
        news_form = UserNewsForm(user=user)
        user_news = News.objects.filter(user=user).order_by('-time_created')
        all_value_users = CustomUser.objects.all().count()
        user_list = CustomUser.objects.exclude(friends_user__user=user)
        user_list_count = CustomUser.objects.exclude(friends_user__user=user).count()
        friendship = user.friends.all()  # с помощью related_name = 'friends' получаем друзей юзера
        avatar_form = UserAvatarForm(instance=user)
        photos_list = Photos.objects.filter(user=user).order_by('-id')  # ищем по юзеру его фото чтобы не перебирать все фото в БД
        user_notifications = Notifications.objects.filter(recipient=user)
        count_notifications = Notifications.objects.filter(recipient=user, is_read=False).count()
        theme = user.themes
        data = {'user': user, 'form': form, 'news_form': news_form, 'user_list': user_list, 'user_list_count': user_list_count, 'friendship': friendship, 'avatar_form': avatar_form, 'photos_list': photos_list, 'all_value_users': all_value_users, 'user_notifications': user_notifications, 'count_notifications': count_notifications, 'user_news': user_news, 'theme': theme}
        if 'search-btn' in request.GET:
            username = request.GET.get('search')
            try:
                users = CustomUser.objects.get(username__icontains=username)
                url = reverse('userprofile', args=[users.username])
                return HttpResponseRedirect(url)
            except Exception as e:
                users = CustomUser.objects.filter(username__icontains=username)
                data['users'] = users
                return render(request, 'login_user/profile.html', data)
        return render(request, 'login_user/profile.html', data)

    def post(self, request):
        user = request.user
        if 'save' in request.POST:
            form = UserChangeForm(request.POST, instance=user)
            if form.is_valid():
                form.last_name = request.POST['last_name']
                form.first_name = request.POST['first_name']
                form.birthday = request.POST['birthday']
                form.about = request.POST['about']
                form.residence = request.POST['residence']
                form.save()
                return redirect('profile')
            else:
                print(form.errors)
        if 'switch-theme' in request.POST:
            files = CustomUser.objects.filter(username=user.username)
            for items in files:
                if items.themes == 'Dark':
                    items.themes = 'Classic'
                    items.save()
                    return redirect('profile')
                else:
                    items.themes = 'Dark'
                    items.save()
                    return redirect('profile')
        if 'likeBtn' in request.POST:
            news_id = request.POST.get('news_id')
            news = News.objects.get(id=news_id)
            if user in news.user_liked.all():
                news.likes -= 1
                news.user_liked.remove(user)
                news.save()
                return redirect('profile')
            else:
                news.likes += 1
                news.user_liked.add(user)
                news.save()
                return redirect('profile')
        if 'addNews' in request.POST:
            form = UserNewsForm(user=user, data=request.POST)
            if form.is_valid():
                form.news = request.POST['news']
                form.save()
                message = f'{user}, запись успешно создана'
                Notifications.objects.create(recipient=user, message=message)
                return redirect('profile')
        if 'delete-news' in request.POST:
            news_id = request.POST.get('newsId')
            news = News.objects.filter(id=news_id)
            news.delete()
            message = f'{user}, запись удалена'
            Notifications.objects.create(recipient=user, message=message)
            return redirect('profile')
        if 'addFriend' in request.POST:
            friend_id = request.POST.get('profile_id')
            friend = get_object_or_404(CustomUser, id=friend_id)
            if user != friend:
                try:
                    friendship = Friendship(user=user, friend=friend)
                    friendship.save()
                    return redirect('profile')
                except Exception as e:
                    print(e)
                    return redirect('profile')
        if 'deleteFriend' in request.POST:
            friend_id = request.POST.get('friend_id')
            friend = get_object_or_404(Friendship, id=friend_id) # или friend = Friendship.objects.filter(id=friend_id)
            friend.delete()
            return redirect('profile')
        if 'addAvatar' in request.POST:
            form = UserAvatarForm(request.POST, request.FILES, instance=user)
            if form.is_valid():
                photos = Photos(user=user)
                avatar_url = request.POST.get('avatar-url')
                photos.photos = avatar_url
                photos.save()
                form.save()
                return redirect('profile')
            else:
                print(form.errors)
            return redirect('profile')
        if 'deletePhoto' in request.POST:
            photo_id = request.POST.get('photo_id')
            photo = Photos.objects.filter(id=photo_id)
            photo.delete()
            return redirect('profile')
        if 'readAll' in request.POST:
            notifications = Notifications.objects.filter(recipient=user)
            for notification in notifications:
                notification.is_read = True
                notification.save()
            return redirect('profile')
        return redirect('profile')

@method_decorator(login_required, name='dispatch')
class NewsView(View):
    def get(self, request):
        user = request.user
        theme = user.themes
        feeds = Feed.objects.all()
        data = {'user': user, 'feeds': feeds, 'theme': theme}
        if 'search-btn' in request.GET:
            username = request.GET.get('search')
            try:
                users = CustomUser.objects.get(username__icontains=username)
                url = reverse('userprofile', args=[users.username])
                return HttpResponseRedirect(url)
            except Exception as e:
                users = CustomUser.objects.filter(username__icontains=username)
                data['users'] = users
                return render(request, 'login_user/news.html', data)
        return render(request, 'login_user/news.html', data)
    def post(self, request):
        if 'parse' in request.POST:
            return self.parse(request)
        if 'clean' in request.POST:
            all_news = Feed.objects.all()
            for news in all_news:
                news.delete()
        if 'likeBtn' in request.POST:
            user = request.user
            feed_id = request.POST.get('feed_id')
            current_feed = Feed.objects.get(id=feed_id)
            if user in current_feed.user_liked.all():
                current_feed.user_liked.remove(user)
                current_feed.likes -= 1
                current_feed.save()
                return redirect('news')
            else:
                current_feed.user_liked.add(user)
                current_feed.likes += 1
                current_feed.save()
                return redirect('news')
        if 'switch-theme' in request.POST:
            theme = CustomUser.objects.filter(username=request.user.username)
            for item in theme:
                if item.themes == 'Dark':
                    item.themes = 'Classic'
                    item.save()
                    return redirect('news')
                else:
                    item.themes = 'Dark'
                    item.save()
                    return redirect('news')
        return redirect('news')

    def parse(self, request):
        url = requests.get('https://lenta.ru/rubrics/culture/')
        soup = BeautifulSoup(url.text, 'html.parser')
        news_links = soup.find_all('a', class_='_longgrid')
        for news in news_links:
            link = news['href']
            news_url = requests.get('https://lenta.ru' + link)
            new_soup = BeautifulSoup(news_url.text, 'html.parser')
            news_title = new_soup.find('span', class_='topic-body__title')
            news_content = new_soup.find_all('p', class_='topic-body__content-text')
            news_pictures = new_soup.find('img', class_='picture__image')
            if news_pictures is not None:
                news_pictures_url = news_pictures['src']
            #base
            feed = Feed()
            feed.news_title = news_title.text
            for i in news_content:
                feed.news_content += i.text + '\n'
            feed.news_pictures = news_pictures_url
            feed.save()
        return redirect('news')


def user_profile(request, user):
    current_user = CustomUser.objects.get(username=user)
    main_user = request.user
    theme = main_user.themes
    news_form = UserNewsForm(user=current_user)
    user_news = News.objects.filter(user=current_user).order_by('-time_created')
    if request.user != current_user:
        friendship = current_user.friends.all()
        photos_list = Photos.objects.filter(user=current_user)
        if request.method == 'POST':
            if 'addNews' in request.POST:
                form = UserNewsForm(user=current_user, data=request.POST)
                if form.is_valid():
                    form.news = request.POST['news']
                    form.save()
                    url = reverse('userprofile', args=[current_user.username])
                    return HttpResponseRedirect(url)
            if 'likeBtn' in request.POST:
                news_id = request.POST.get('news_id')
                news = News.objects.get(id=news_id)
                if main_user in news.user_liked.all():
                    news.likes -= 1
                    news.user_liked.remove(main_user)
                    news.save()
                    url = reverse('userprofile', args=[current_user.username])
                    return HttpResponseRedirect(url)
                else:
                    news.likes += 1
                    news.user_liked.add(main_user)
                    news.save()
                    message = f'{main_user} оценил вашу запись'
                    Notifications.objects.create(recipient=current_user, message=message)
                    url = reverse('userprofile', args=[current_user.username])
                    return HttpResponseRedirect(url)
        return render(request, 'login_user/user_profile.html', {'user': current_user, 'friendship': friendship, 'photos_list': photos_list, 'news': news_form, 'main_user': main_user, 'user_news': user_news, 'theme': theme})
    else:
        return redirect('profile')

def notifications_user_registered(sender, user, request, **kwargs):
    UserModel = get_user_model()
    user = UserModel.objects.get(username=user.username)
    news = f'{user} зарегистрировался'
    create_news = News.objects.create(user=user, news=news)
    message = f'{user}, ваш аккаунт внесён в базу'
    Notifications.objects.create(recipient=user, message=message)

def notifications_user_activated(sender, user, request, **kwargs):
    UserModel = get_user_model()
    user = UserModel.objects.get(username=user.username)
    message =f'{user}, ваш аккаунт успешно активирован'
    Notifications.objects.create(recipient=user, message=message)
def notification_user_logged(sender, user, request, **kwargs):
    message = f'{request.user}, в ваш аккаунт был выполнен вход'
    Notifications.objects.create(recipient=request.user, message=message)
    return redirect('profile')
def notification_user_logout(sender, user, request, **kwargs):
    message = f'{request.user}, Вы вышли из аккаунта'
    Notifications.objects.create(recipient=request.user, message=message)
    return redirect('profile')

user_registered.connect(notifications_user_registered)
user_activated.connect(notifications_user_activated)
user_logged_in.connect(notification_user_logged)
user_logged_out.connect(notification_user_logout)
# Create your views here.
