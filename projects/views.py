from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .utils import search_projects
from .models import Project
from .forms import ProjectForm

def projects(request):
    search_query, projects = search_projects(request)
    page = request.GET.get('page', 1)
    results = 3
    paginator = Paginator(projects, results)
    try:
        projects = paginator.page(page)
    except EmptyPage:
        if int(page) <= 0:
            projects = paginator.page(1)
        else:
            projects = paginator.page(paginator.num_pages)

    except PageNotAnInteger:
        projects = paginator.page(1)

    context = {
        'projects' : projects,
        'search_query' : search_query,
    }
    return render(request, 'projects/projects.html', context)

def project(request, pk):
    project_obj = get_object_or_404(Project, pk=pk)
    tags = project_obj.tags.all()

    context = {
        'project_obj' : project_obj,
        'tags' : tags
    }
    return render(request, 'projects/single_project.html', context)

@login_required(login_url='login')
def create_project(request):
    profile = request.user.profile
    form = ProjectForm()
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            return redirect(reverse('project', args=[project.id]))

    context = {
        'form' : form
    }
    return render(request, 'projects/project_form.html', context)

@login_required(login_url='login')
def update_project(request, pk):
    profile = request.user.profile
    project_obj = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project_obj)

    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES, instance=project_obj)
        if form.is_valid():
            form.save()
            return redirect(reverse('project', args=[project_obj.id]))

    context = {
        'form': form
    }
    return render(request, 'projects/project_form.html', context)


@login_required(login_url='login')
def delete_project(request, pk):
    profile = request.user.profile
    project_obj = profile.project_set.get(id=pk)

    if request.method == 'POST':
        project_obj.delete()
        return redirect('my-account')

    context = {
        'object' : project_obj
    }
    return render(request, 'delete_template.html', context)
