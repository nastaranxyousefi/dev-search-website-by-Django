from django.db.models import Q

from .models import Profile, Skill


def search_profiles(request):
    search_query = request.GET.get('q') or ''
    skills = Skill.objects.filter(name__icontains=search_query)
    profiles = Profile.objects.distinct().filter(
        Q(name__icontains=search_query) |
        Q(short_intro__icontains=search_query) |
        Q(skill__in=skills)
    )
    return search_query, profiles
