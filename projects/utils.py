from django.db.models import Q

from .models import Project

def search_projects(request):
    search_query = request.GET.get('q') or ''
    projects = Project.objects.distinct().filter(
        Q(title__icontains=search_query) |
        Q(description__icontains=search_query) |
        Q(owner__name__icontains=search_query) |
        Q(tags__name__icontains=search_query)
    )

    return search_query, projects
