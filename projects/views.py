from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Project,Task,ProjectFile

@login_required(login_url='/login/')
def project_list(request):
    if request.user.is_staff:
        projects = Project.objects.all().order_by('-created_at')
    else:
        projects = request.user.projects.all().order_by('-created_at')

    return render(request, 'projects/project_list.html',{
        'projects' : projects,
    })

@login_required(login_url='/login/')
def project_create(request):
    if not request.user.is_staff:
        messages.error(request, 'Only Admin can create projects!')
        return redirect('/projects/')
    
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST.get('description', '')
        deadline = request.POST['deadline']
        student_ids = request.POST.getlist('students')

        project = Project.objects.create(
            title=title,
            description=description,
            deadline=deadline,
            created_by=request.user,
        )
        project.students.set(student_ids)
        messages.success(request, 'Project created!')

    students = User.objects.filter(is_staff=False)
    return render(request, 'projects/project_create.html',{
        'students' : students,
    })

@login_required(login_url='/login/')
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    tasks = project.tasks.all()
    files = project.files.all()

    return render(request, 'projects/project_detail.html', {
        'project' : project,
        'tasks' : tasks,
        'files' : files,
    })

@login_required(login_url='/login/')
def task_add(request, pk):
    if not request.user.is_staff:
        messages.error(request, 'Only Admin can add tasks!')
        return redirect(f'/projects/{pk}/')
    
    project = get_object_or_404(Project, pk=pk)
    
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST.get('description', '')
        assigned_to_id = request.POST['assigned_to']
        deadline = request.POST['deadline']
        
        assigned_to = User.objects.get(pk=assigned_to_id)
        Task.objects.create(
            project=project,
            title=title,
            description=description,
            assigned_to=assigned_to,
            deadline=deadline,
        )
        messages.success(request, 'Task added!')
        return redirect(f'/projects/{pk}/')
    
    # Sirf is project ke students nahi — SAARE students dikhao
    students = User.objects.filter(is_staff=False)  # ← YEH FIX HAI
    return render(request, 'projects/task_add.html', {
        'project': project,
        'students': students,
    })

@login_required(login_url='/login/')
def file_upload(request, pk):
    project = get_object_or_404(Project,pk=pk)

    if request.method == 'POST':
        file = request.FILES.get('file')
        if file:
            ProjectFile.objects.create(
                project=project,
                uploaded_by = request.user,
                file = file,
            )
            messages.success(request,'file uploaded!')
        return redirect(f'/projects/{pk}/')
    
    return redirect(f'/projects/{pk}/')

@login_required(login_url='/login/')
def task_complete(request,pk):
    task = get_object_or_404(Task , pk=pk)
    task.status = 'completed'
    task.save()
    messages.success(request, 'Task marked as completed!')
    return redirect(f'/projects/{task.project.pk}/')

@login_required(login_url='/login/')
def project_edit(request, pk):
    if not request.user.is_staff:
        messages.error(request, 'Only Admin can edit projects!')
        return redirect('/projects/')
    
    project = get_object_or_404(Project, pk=pk)
    students = User.objects.filter(is_staff=False)
    
    if request.method == 'POST':
        project.title = request.POST['title']
        project.description = request.POST.get('description', '')
        project.deadline = request.POST['deadline']
        student_ids = request.POST.getlist('students')
        project.students.set(student_ids)
        project.save()
        messages.success(request, 'Project updated!')
        return redirect(f'/projects/{pk}/')
    
    return render(request, 'projects/project_edit.html', {
        'project': project,
        'students': students,
    })

@login_required(login_url='/login/')
def project_delete(request, pk):
    if not request.user.is_staff:
        messages.error(request, 'Only Admin can delete projects!')
        return redirect('/projects/')
    
    project = get_object_or_404(Project, pk=pk)
    project.delete()
    messages.success(request, 'Project deleted!')
    return redirect('/projects/')