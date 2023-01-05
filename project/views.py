from django.shortcuts import render, redirect
from .models import Project
from .forms import ProjectForm

def projects(request):
    projects = Project.objects.all()
    context = {'projects': projects}
    return render(request, 'project/projects.html', context)

def project(request, pk):
    project = Project.objects.get(id=pk)
    context = {'project': project}
    return render(request, 'project/project.html', context)

def createproject(request):
    form = ProjectForm()

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('projects')
    context = {'form': form}
    return render(request, 'project/project_form.html', context)

def updateproject(request, pk):
    project = Project.objects.get(id=pk)
    form = ProjectForm(instance=project)   
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('projects')
    context = {'form': form}
    return render(request, 'project/project_form.html', context)

def deleteproject(request, pk):
    project = Project.objects.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('projects')
    return render(request, 'project/delete.html', {'obj': project})
