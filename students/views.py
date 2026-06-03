from django.shortcuts import render , redirect , get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Student, Attendance , Result
from django.utils import timezone
from django.contrib.auth.models import User
@login_required(login_url='/login/')
def student_list(request):
    search = request.GET.get('search' , '')
    students = Student.objects.all()

    if search:
        students = students.filter(name__icontains=search)

    students = students.order_by('name')

    return render(request , 'students/student_list.html' ,{
        'students': students,
        'search' : search, 
    })

@login_required(login_url='/login/')
def student_add(request):
    if not request.user.is_staff:
        messages.error(request, 'Only Admin can add students!')
        return redirect('/students/')
    
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST.get('phone' , '')
        gender = request.POST['gender']
        date_of_birth = request.POST.get('date_of_birth' , '')
        address = request.POST['address']
        class_name = request.POST['class_name']
        roll_number = request.POST['roll_number']

        if Student.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists!')
            return redirect('/students/add/')

        if Student.objects.filter(roll_number = roll_number).exists():
            messages.error(request, 'Roll number already exists!')
            return redirect('/students/add/')

        Student.objects.create(
            name=name,
            email=email,
            phone=phone,
            gender=gender,
            date_of_birth=date_of_birth if date_of_birth else None,
            address=address,
            class_name=class_name,
            roll_number=roll_number,
        )        
# Auto login account banana
        if not User.objects.filter(username=name).exists():
            User.objects.create_user(
                username=name,
                password=str(roll_number)
            )

        messages.success(request, 'Student added! Login: username={}, password={}'.format(name, roll_number))
        return redirect('/students/')

    
    return render(request, 'students/student_add.html')



@login_required(login_url='/login/')
def student_edit(request,pk):
    if not request.user.is_staff:
        messages.error(request, 'Only Admin can edit students!')
        return redirect('/students/')
    student = get_object_or_404(Student,pk=pk)

    if request.method == 'POST':
        student.name = request.POST['name']
        student.email = request.POST['email']
        student.phone = request.POST.get('phone', '')
        student.gender = request.POST['gender']
        student.address = request.POST.get('address', '')
        student.class_name = request.POST['class_name']
        student.roll_number = request.POST['roll_number']
        date_of_birth = request.POST.get('date_of_birth', '')
        student.date_of_birth = date_of_birth if date_of_birth else None
        student.save()
        messages.success(request, 'Student updated!')
        return redirect('/students/')
    return render(request, 'students/student_edit.html' , {'student':student})

@login_required(login_url='/login/')
def student_delete(request,pk):
    if not request.user.is_staff:
        messages.error(request, 'Only Admin can delete students!')
        return redirect('/students/')
    student = get_object_or_404(Student , pk=pk)
    student.delete()
    messages.success(request,'Student deleted!')
    return redirect('/students/')

@login_required(login_url='/login/')
def student_detail(request,pk):
    student = get_object_or_404(Student,pk=pk)
    attendances = student.attendances.all().order_by('-date')
    results = student.results.all().order_by('-exam_date')

    return render(request, 'students/student_detail.html',{
        'student' : student,
        'attendances' : attendances,
        'results' : results,
    })
   
@login_required(login_url='/login/')
def attendance_add(request, pk):
    student = get_object_or_404(Student, pk=pk)
    today = timezone.now().date()

    if request.method == 'POST':
        date = request.POST['date']
        status = request.POST['status']
        remarks = request.POST.get('remarks', '')

        if Attendance.objects.filter(student=student, date=date).exists():
            messages.error(request, 'Attendance already marked for this date!')
            return redirect(f'/students/{pk}/')

        Attendance.objects.create(
            student=student,
            date=date,
            status=status,
            remarks=remarks,
        )
        messages.success(request, 'Attendance marked!')
        return redirect(f'/students/{pk}/')

    return render(request, 'students/attendance_add.html', {
        'student': student,
        'today':timezone.now().date().strftime('%Y-%m-%d'),
    })


@login_required(login_url='/login/')
def result_add(request, pk):
    student = get_object_or_404(Student, pk=pk)

    if request.method == 'POST':
        subject = request.POST['subject']
        marks_obtained = request.POST['marks_obtained']
        total_marks = request.POST['total_marks']
        grade = request.POST['grade']
        exam_date = request.POST['exam_date']

        Result.objects.create(
            student=student,
            subject=subject,
            marks_obtained=marks_obtained,
            total_marks=total_marks,
            grade=grade,
            exam_date=exam_date,
        )
        messages.success(request, 'Result added!')
        return redirect(f'/students/{pk}/')

    return render(request, 'students/result_add.html', {'student': student})
