from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .forms import UserChangeForm, UserNewsForm
from .models import News
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
            news = get_object_or_404(News, id=news_id)
            news.likes += 1
            news.user_liked = user.username # добавляем юзернейм лайкнувшего, доделатЬ!
            news.save()
        if 'addNews' in request.POST:
            form = UserNewsForm(user=user, data=request.POST)
            if form.is_valid():
                form.news = request.POST['news']
                form.save()
                return redirect('profile')
        if 'delete-news' in request.POST:
            news_id = request.POST.get('newsId')
            news = News.objects.filter(id=news_id)
            news.delete()
            return redirect('profile')
    return render(request, 'login_user/profile.html', {'user': user, 'form': form, 'news_form': news_form})

# Create your views here.
