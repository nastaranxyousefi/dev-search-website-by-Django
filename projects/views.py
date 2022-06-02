from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404

from .models import Project, Tag
from .forms import ProjectForm

def projects(request):
    all_projects = Project.objects.all()
    context = {
        'projects' : all_projects,
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


def create_project(request):
    form = ProjectForm()
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('projects')

    context = {
        'form' : form
    }
    return render(request, 'projects/project_form.html', context)
