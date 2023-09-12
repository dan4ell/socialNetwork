from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.forms import UserChangeForm
from .forms import UserChangeForm
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
    return render(request, 'login_user/profile.html', {'user': user})

@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        if 'save_form' in request.POST:
            form = UserChangeForm(request.POST, instance=user) # используем текущего юзера в качестве экземпляра формы
            if form.is_valid():
                form.last_name = request.POST['last_name']
                form.first_name = request.POST['first_name']
                form.save()
                return redirect('profile')
            else:
                print(form.errors)
        else:
            return redirect('edit_profile')
    form = UserChangeForm(instance=user)
    return render(request, 'login_user/edit_profile.html', {'form': form})

# Create your views here.
