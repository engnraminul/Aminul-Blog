from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from Login_App.forms import SignUpForm, UserProfileUpdate, ProfileImage


def signup(request):
    form = SignUpForm()
    registered = False
    if request.method == 'POST':
        form = SignUpForm(data=request.POST)
        if form.is_valid():
            form.save()
            registered = True

    context = {'form':form, 'registered':registered}
    return render(request, 'Login_App/signup.html', context = context)


def login_page(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('Blog_App:post_list'))

    return render(request, 'Login_App/login.html', context={'form':form})

@login_required
def log_out(request):
    logout(request)
    return HttpResponseRedirect(reverse('Blog_App:post_list'))


@login_required

def profile(request):
    return render(request, 'Login_App/profile.html')

@login_required
def profile_update(request):
    current_user = request.user
    form = UserProfileUpdate(instance=current_user)
    if request.method == 'POST':
        form = UserProfileUpdate(request.POST, instance=current_user)
        if form.is_valid():
            form.save()
            form = UserProfileUpdate(instance=current_user)
    return render(request, 'Login_App/profile_update.html', context={'form':form})

@login_required
def password_change(request):
    current_user = request.user
    changed = False
    form = PasswordChangeForm(current_user)
    if request.method == 'POST':
        form = PasswordChangeForm(current_user, data=request.POST)
        if form.is_valid():
            form.save()
            changed = True
    return render(request, 'Login_App/password_change.html', context={'form':form, 'changed':changed})



@login_required
def add_profile_Image(request):
    form = ProfileImage()
    if request.method == 'POST':
        form = ProfileImage(request.POST, request.FILES)
        if form.is_valid():
            user_obj = form.save(commit=False)
            user_obj.user = request.user
            user_obj.save()
            return HttpResponseRedirect(reverse('Login_App:profile'))
    return render(request, 'Login_App/add_profile_Image.html', context={'form':form})


@login_required
def change_profile_image(request):
    form = ProfileImage(instance=request.user.user_profile)
    if request.method == 'POST':
        form = ProfileImage(request.POST, request.FILES, instance=request.user.user_profile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('Login_App:profile'))
    return render(request, 'Login_App/add_profile_Image.html', context={'form':form})
