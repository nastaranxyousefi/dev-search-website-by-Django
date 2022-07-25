from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from .forms import CustomUserCreationForm, ProfileForm, SkillForm
from .models import Profile, Message
from projects.models import Project
from .utils import search_profiles


def login_page(request):
    page = 'login'
    if request.user.is_authenticated: #restrict a logged-in user from seeing login url.
        return redirect('profiles')

    if request.method == 'POST':
        #set the request.post elements to username & password
        username = request.POST['username'].lower()
        password = request.POST['password']

        #make sure the user exists:
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "The username doesn't exist.")

        user = authenticate(request, username=username, password=password)   #make sure password matches the user. return user instance or None

        if user is not None:
            login(request, user) #Create a session for this user in the database.
            return redirect(request.GET['next'] if 'next' in request.GET else 'my-account')
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
    form = CustomUserCreationForm()
    page = 'register'

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'User account was created!')
            login(request, user)
            return redirect('edit-account')
        else:
            messages.error(request, 'An error has occurred during the registration.')

    context = {
        'page': page,
        'form' : form,
    }
    return render(request, 'users/login_registration.html', context)


def profiles(request):
    search_query , profiles = search_profiles(request)
    page = request.GET.get('page', 1)
    results = 6
    paginator = Paginator(profiles, results)
    try:
        profiles = paginator.page(page)
    except EmptyPage:
        if int(page) <= 0:
            profiles = paginator.page(1)
        else:
            profiles = paginator.page(paginator.num_pages)

    except PageNotAnInteger:
        profiles = paginator.page(1)
    context = {
        'profiles' : profiles,
        'search_query' : search_query,
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

@login_required(login_url='login')
def user_account(request):
    profile = request.user.profile
    skills = profile.skill_set.all()
    projects = profile.project_set.all()
    context = {
        'profile' : profile,
        'skills' : skills,
        'projects' : projects,
    }
    return render(request, 'users/account.html', context)


@login_required(login_url='login')
def edit_account(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('my-account')

    context = {
        'form' : form,
    }
    return render(request, 'users/profile_form.html', context)


@login_required(login_url='login')
def create_skill(request):
    profile = request.user.profile
    form = SkillForm()

    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, 'Skill was added successfully')
            return redirect('my-account')

    context = {
        'form' : form,
    }
    return render(request, 'users/skill_form.html', context)


@login_required(login_url='login')
def update_skill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)

    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, 'Skill was updated successfully')
            return redirect('my-account')

    context = {
        'form' : form,
    }
    return render(request, 'users/skill_form.html', context)


@login_required(login_url='login')
def delete_skill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)

    if request.method == "POST":
        skill.delete()
        messages.success(request, 'Skill was deleted successfully')
        return redirect('my-account')

    context = {
        'object' : skill,
    }
    return render(request, 'delete_template.html', context)


@login_required(login_url='login')
def inbox_view(request):
    profile = request.user.profile
    read_messages = profile.messages.exclude(is_read=False)
    unread_messages = profile.messages.filter(is_read=False)
    unread_messages_count = unread_messages.count()

    context = {
        'read_messages' : read_messages,
        'unread_messages' : unread_messages,
        'unread_messages_count' : unread_messages_count
    }

    return render(request, 'users/inbox.html', context)


def view_message(requset):
    return render(requset, 'users/message.html')