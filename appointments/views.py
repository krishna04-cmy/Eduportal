from django.shortcuts import render , redirect ,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Appointment

@login_required(login_url='/login/')
def appointment_list(request):
    if request.user.is_staff:
        appointments = Appointment.objects.all().order_by('-created_at')
    else:
        appointments = Appointment.objects.filter(student=request.user).order_by('-created_at')

    return render(request,'appointments/appointment_list.html' , {
        'appointments': appointments,
    })

@login_required(login_url='/login/')
def appointment_book(request):
    if request.user.is_staff:
        messages.error(request,'Admin cannot book appointments!')
        return redirect('/appointments/')
    

    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST.get('description' , '')
        date = request.POST['date']
        time = request.POST['time']

        Appointment.objects.create(
            student = request.user,
            title = title,
            description = description,
            date = date,
            time = time,
        )
        messages.success(request,'Appointment booked! wait for admin approval.')
        return redirect('/appointments/')
    
    return render(request, 'appointments/appointment_book.html')

@login_required(login_url='/login/')
def appointment_approve(request,pk):
    if not request.user.is_staff:
        messages.error(request, 'Only Admin can approve!')
        return redirect('/appointments/')
    
    appointment = get_object_or_404(Appointment, pk=pk)
    appointment.status = 'approved'
    appointment.admin_note = request.POST.get('admin_note' , '')
    appointment.save()
    messages.success(request,'Appointment approved!')
    return redirect('/appointments/')

@login_required(login_url='/login/')
def appointment_reject(request,pk):
    if not request.user.is_staff:
        messages.error(request, 'Only Admin can reject!')
        return redirect('/appointments/')
    
    appointment =get_object_or_404(Appointment, pk=pk)
    appointment.status = 'rejected'
    appointment.admin_note = request.POST.get('admin_note' , '')
    appointment.save()
    messages.success(request , 'Appointment rejected!')
    return redirect('/appointments/')