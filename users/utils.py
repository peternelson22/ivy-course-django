from django.db.models import Q
from .models import Profile, Skill
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def paginate_profile(request, profile, results):

    page = request.GET.get('page')
    paginator = Paginator(profile, results)

    try:
        profile = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        profile = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        profile = paginator.page(page)

    left_index = (int(page) - 4)
    if left_index < 1:
        left_index = 1

    right_index = (int(page) + 5)

    if right_index > paginator.num_pages:
        right_index = paginator.num_pages + 1

    custom_range = range(left_index, right_index)

    return custom_range, profile


def search_profile(request):
    search_query = ''
    if request.GET.get('search'):
            search_query = request.GET.get('search')

    skills = Skill.objects.filter(name__icontains=search_query)

    profile = Profile.objects.distinct().filter(Q(name__icontains=search_query) | 
                                                        Q(intro__icontains=search_query) |
                                                        Q(skill__in=skills))

    return profile, search_query
