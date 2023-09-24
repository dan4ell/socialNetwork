from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import UserChangeForm, UserNewsForm, UserAvatarForm
from .models import News, CustomUser, Friendship, Photos, Notifications
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django_registration.signals import user_registered, user_activated
from django.contrib.auth import get_user_model
def index(request):
    return redirect('profile')

def pw_reset_done(request):
    return render(request, 'django_registration/password_reset_done.html')
def reset_is_done(request):
    return render(request, 'django_registration/password_reset_is_done.html')

def redirect_profile(request):
    return redirect('profile')

@login_required
def profile(request):
    user = request.user
    form = UserChangeForm(instance=user)
    news_form = UserNewsForm(user=user)
    all_value_users = CustomUser.objects.all().count()
    user_list = CustomUser.objects.exclude(friends_user__user=user)
    user_list_count = CustomUser.objects.exclude(friends_user__user=user).count()
    print(user_list)
    friendship = user.friends.all() # с помощью related_name = 'friends' получаем друзей юзера
    avatar_form = UserAvatarForm(instance=user)
    photos = Photos(user=user)
    photos_list = Photos.objects.filter(user=user) # ищем по юзеру его фото чтобы не перебирать все фото в БД
    recipient = user
    user_notifications = Notifications.objects.filter(recipient=recipient)
    count_notifications = Notifications.objects.filter(recipient=recipient, is_read=False).count()
    if request.method == 'POST':
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
                news.user_liked.add(user) # добавляем юзернейм лайкнувшего, доделатЬ!
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
    return render(request, 'login_user/profile.html', {'user': user, 'form': form, 'news_form': news_form, 'user_list': user_list, 'user_list_count': user_list_count, 'friendship': friendship, 'avatar_form': avatar_form, 'photos_list': photos_list, 'all_value_users': all_value_users, 'user_notifications': user_notifications, 'count_notifications': count_notifications})

def user_profile(request, user):
    current_user = CustomUser.objects.get(username=user)
    main_user = request.user
    news_form = UserNewsForm(user=current_user)
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
                    url = reverse('userprofile', args=[current_user.username])
                    return HttpResponseRedirect(url)
        return render(request, 'login_user/user_profile.html', {'user': current_user, 'friendship': friendship, 'photos_list': photos_list, 'news': news_form, 'main_user': main_user})
    else:
        return redirect('profile')

def notifications_user_registered(sender, user, request, **kwargs):
    UserModel = get_user_model()
    user = UserModel.objects.get(username=user.username)
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
