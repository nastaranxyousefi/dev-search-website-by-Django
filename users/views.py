from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

from .models import Profile
from projects.models import Project


def login_page(request):
    page = 'login'

    if request.user.is_authenticated: #restrict a logged-in user from seeing login url.
        return redirect('profiles')

    if request.method == 'POST':
        #set the request.post elements to username & password
        username = request.POST['username']
        password = request.POST['password']

        #make sure the user exists:
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "The username doesn't exist.")

        user = authenticate(request, username=username, password=password)   #make sure password matches the user. return user instance or None

        if user is not None:
            login(request, user) #Create a session for this user in the database.
            return redirect('profiles')
        else:
            messages.error(request, 'Username or password is incorrect.')


    context = {
        'page' : page,
    }
    return render(request, 'users/login_registration.html')


def logout_user(request):
    logout(request) #delete that session
    messages.info(request, 'User was logged out.')
    return redirect('login')


def register_user(request):
    form = UserCreationForm()
    page = 'register'

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'User account was created!')
            login(request, user)
            return redirect('profiles')
        else:
            messages.error(request, 'An error has occurred during the registration.')

    context = {
        'page': page,
        'form' : form,
    }
    return render(request, 'users/login_registration.html', context)


def profiles(request):
    profiles = Profile.objects.all()
    context = {
        'profiles' : profiles,
    }
    return render(request, 'users/profiles.html', context)


def user_profile(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    top_skills = profile.skill_set.exclude(description__exact="")
    other_skills = profile.skill_set.filter(description="")
    projects = Project.objects.filter(owner=profile)
    context = {
        'profile' : profile,
        'top_skills' : top_skills,
        'other_skills' : other_skills,
        'projects' : projects,
    }
    return render(request, 'users/user-profile.html', context)