from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required


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

@login_required(login_url='login')
def create_project(request):
    form = ProjectForm()
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('projects')

    context = {
        'form' : form
    }
    return render(request, 'projects/project_form.html', context)

@login_required(login_url='login')
def update_project(request, pk):
    project_obj = Project.objects.get(id=pk)
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
    project_obj = Project.objects.get(id=pk)

    if request.method == 'POST':
        project_obj.delete()
        return redirect('projects')

    context = {
        'project' : project_obj
    }
    return render(request, 'projects/delete_project.html', context)