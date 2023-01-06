from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Project
from .utils import search_project, paginate_project 
from .forms import ProjectForm

@login_required(login_url='login')
def projects(request):
    
    projects, search_query = search_project(request)
    custom_range, projects = paginate_project(request, projects, 6) 
   
    context = {'projects': projects,
               'search': search_query, 'custom_range': custom_range}
    return render(request, 'project/projects.html', context)


@login_required(login_url='login')
def project(request, pk):
    project = Project.objects.get(id=pk)
    context = {'project': project}
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
