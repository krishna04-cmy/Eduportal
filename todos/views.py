from django.shortcuts import render , redirect , get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Todo

@login_required(login_url = '/login/')   # user login nhi toh login page pr bhej do
def todo_list(request):                   # all function show
    search = request.GET.get('search', '') #url se search value lane
    status_filter = request.GET.get('status','') #url se status le rha

    todos = Todo.objects.filter(user=request.user) # login user ke task-fetch oter uer k task nhi

    if search:                                     #user ne search kiya
        todos = todos.filter(title__icontains=search)  #search nd icontains-> case insensitive

    if status_filter:                                  # satus selected hai toh
        todos = todos.filter(status=status_filter)      # status ke basis pr folter (pending,comleted)

    todos = todos.order_by('-created_at')  # latest task pehle shoe ( - mean descending order)

    return render(request, 'todos/todo_list.html',{
        'todos' : todos,
        'search' : search,
        'status_filter' : status_filter,
    })

@login_required(login_url='/login/')
def todo_add(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST.get('description','')

        if not title:
            messages.error(request,'Tital is required!')
            return redirect('/todos/')
        
        Todo.objects.create(
            user=request.user,
            title = title,
            description = description,
        )

        messages.success(request,'Task added!')
        return redirect('/todos/')

@login_required(login_url='/login/')
def todo_update(request, pk):
    todo = get_object_or_404(Todo,pk=pk, user=request.user)

    if request.method == 'POST':
        todo.title = request.POST['title']
        todo.description = request.POST.get('description' ,'')
        todo.status = request.POST['status']
        todo.save()
        messages.success(request, 'Task updated!')
        return redirect('/todos/')
    
    return render(request, 'todos/todo_edit.html' , {'todo':todo})

@login_required(login_url='/login/')
def todo_delete(request , pk):
    todo = get_object_or_404(Todo , pk=pk , user=request.user)
    todo.delete()
    messages.success(request, 'Task deleted!')
    return redirect('/todos/')

@login_required(login_url='/login/')
def todo_toggle(request, pk):
    todo = get_object_or_404(Todo, pk=pk,user=request.user)
    if todo.status == 'pending':
        todo.status = 'completed'
    else:
        todo.status = 'pending'
    todo.save()
    return redirect('/todos/')
