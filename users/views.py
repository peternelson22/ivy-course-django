from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile
from .utils import search_profile, paginate_profile
from .forms import CustomUserCreationForm, ProfileForm, SkillForm

def register_(request):
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
           user = form.save(commit=False)
           user.username = user.username.lower()
           user.save()
           messages.success(request, 'User created successfully')

           login(request, user)
           return redirect('edit-account')

        else:
            messages.error(request, 'Something went wrong')

    context = {'form': form}
    return render(request, 'users/login-register.html', context)


def login_(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('profile')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, 'Something went wrong')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            messages.error(request, 'Bad Credentials')

    return render(request, 'users/login-register.html', {'page': page})

def logout_(request):
    logout(request)
    messages.info(request, 'User successfully logout')
    return redirect('login')

@login_required(login_url='login')
def profile(request):

    profile, search_query = search_profile(request) 
    custom_range, profile = paginate_profile(request, profile, 6)
   
    context = {'profiles': profile, 'search': search_query, 'custom_range': custom_range}
    return render(request, 'users/profile.html', context)


@login_required(login_url='login')
def userprofile(request, pk):
    profile = Profile.objects.get(pk=pk)
    top_skills = profile.skill_set.exclude(description__exact='')
    other_skills = profile.skill_set.filter(description='')
    context = {'profile': profile, 'top_skills': top_skills, 'other_skills': other_skills}
    return render(request, 'users/user-profile.html', context)


@login_required(login_url='login')
def useraccount(request):
    profile = request.user.profile
    projects = profile.project_set.all()

    skills = profile.skill_set.all()

    context = {'profile': profile, 'skills': skills, 'projects': projects}
    return render(request, 'users/account.html', context)


@login_required(login_url='login')
def edit_account(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account')

    context = {'form': form}
    return render(request, 'users/profile-form.html', context)


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
            return redirect('account')

    context = {'form': form}
    return render(request, 'users/skill-form.html', context)


@login_required(login_url='login')
def update_skill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)

    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save(commit=False)
            form.save()
            messages.success(request, 'Skill was updated successfully')
            return redirect('account')

    context = {'form': form}
    return render(request, 'users/skill-form.html', context)

def delete_skill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)

    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Skill was deleted successfully')
        return redirect('account')

    return render(request, 'delete.html', {'obj': skill})