from django.shortcuts import render
from django.shortcuts import get_object_or_404

from .models import Profile
from projects.models import Project


def login_page(request):
    return render(request, 'users/login_registration.html')


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