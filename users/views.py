from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from .models import Profile
from projects.models import Project


def login_page(request):
    if request.method == 'POST':
        #set the request.post elements to username & password
        username = request.POST['username']
        password = request.POST['password']

        #make sure the user exists:
        try:
            user = User.objects.get(username=username)
        except:
            print("the username doesn't exist.")

        user = authenticate(request, username=username, password=password)   #make sure password matches the user. return user instance or None

        if user is not None:
            login(request, user) #Create a session for this user in the database.
            return redirect('profiles')
        else:
            print('the username and password is incorrect.')

    return render(request, 'users/login_registration.html')


def logout_user(request):
    logout(request) #delete that session
    return redirect('login')

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