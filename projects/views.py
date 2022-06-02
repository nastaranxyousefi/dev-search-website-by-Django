from django.shortcuts import render
from django.shortcuts import get_object_or_404

from .models import Project

def projects(request):
    all_projects = Project.objects.all()
    context = {
        'projects' : all_projects,
    }
    return render(request, 'projects/projects.html', context)

def project(request, pk):
    project_obj = get_object_or_404(Project, pk=pk)

    context = {
        'project_obj' : project_obj
    }
    return render(request, 'projects/single_project.html', context)
