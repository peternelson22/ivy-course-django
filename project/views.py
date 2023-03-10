from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Project
from .utils import search_project, paginate_project 
from .forms import ProjectForm, ReviewForm

def projects(request):
    
    projects, search_query = search_project(request)
    custom_range, projects = paginate_project(request, projects, 6) 
   
    context = {'projects': projects,
               'search': search_query, 'custom_range': custom_range}
    return render(request, 'project/projects.html', context)


def project(request, pk):
    project_obj = Project.objects.get(id=pk)
    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = project_obj
        review.owner = request.user.profile
        review.save()

        project_obj.getvotecount

        messages.success(request, 'Your review was successfully submitted')
        return redirect('project', pk=project_obj.id)



    context = {'project': project_obj, 'form': form}
    return render(request, 'project/project.html', context)


@login_required(login_url='login')
def createproject(request):
    profile = request.user.profile
    form = ProjectForm()

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            return redirect('account')
    context = {'form': form}
    return render(request, 'project/project_form.html', context)

@login_required(login_url='login')
def updateproject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)   
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('account')
    context = {'form': form}
    return render(request, 'project/project_form.html', context)


@login_required(login_url='login')
def deleteproject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('projects')
    return render(request, 'delete.html', {'obj': project})
