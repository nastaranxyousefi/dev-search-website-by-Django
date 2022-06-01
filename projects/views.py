from django.shortcuts import render


def projects(request):
    return render(request, 'projects/projects.html')

def project(request, pk):
    return render(request, 'projects/single_project.html')
