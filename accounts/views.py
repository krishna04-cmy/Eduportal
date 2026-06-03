from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from students.models import Student , Attendance
from blog.models import Post
from todos.models import Todo
from django.utils import timezone
import calendar


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/dashboard/')
            else:
                messages.error(request, 'Please verify your email first!')
        else:
            messages.error(request, 'Wrong username or password!')
    return render(request, 'auth/login.html')


def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, 'Passwords do not match!')
            return redirect('/register/')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken!')
            return redirect('/register/')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered!')
            return redirect('/register/')

        user = User.objects.create_user(username=username, email=email, password=password1)
        user.is_active = True
        user.save()
        messages.success(request, 'Account created! Please Login.')
        return redirect('/login/')

    return render(request, 'auth/register.html')


def logout_view(request):
    logout(request)
    return redirect('/login/')


@login_required(login_url='/login/')


@login_required(login_url='/login/')
def dashboard_view(request):
    today = timezone.now().date()
    current_month = today.month
    current_year = today.year

    if request.user.is_staff:
        total_students = Student.objects.count()
        total_teachers = User.objects.filter(is_staff=True).count()
        
        # Current month ki attendance
        total_attendance = Attendance.objects.filter(
            date__month=current_month, date__year=current_year
        ).count()
        present_attendance = Attendance.objects.filter(
            date__month=current_month, date__year=current_year, status='present'
        ).count()
        
        total_blog_posts = Post.objects.filter(status='published').count()
        total_tasks = Todo.objects.filter(user=request.user).count()

    else:
        try:
            student = Student.objects.get(name=request.user.username)
            
            # Current month ki sirf us student ki attendance
            total_attendance = Attendance.objects.filter(
                student=student,
                date__month=current_month,
                date__year=current_year
            ).count()
            present_attendance = Attendance.objects.filter(
                student=student,
                date__month=current_month,
                date__year=current_year,
                status='present'
            ).count()
        except Student.DoesNotExist:
            total_attendance = 0
            present_attendance = 0

        total_students = 1
        total_teachers = User.objects.filter(is_staff=True).count()
        total_blog_posts = Post.objects.filter(status='published').count()
        total_tasks = Todo.objects.filter(user=request.user).count()

    if total_attendance > 0:
        attendance_percent = round((present_attendance / total_attendance) * 100)
    else:
        attendance_percent = 0

    return render(request, 'dashboard/dashboard.html', {
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_courses': 0,
        'total_attendance': attendance_percent,
        'total_blog_posts': total_blog_posts,
        'total_tasks': total_tasks,
        'current_month': today.strftime('%B %Y'),  # e.g. "June 2026"
    })

#-----------------------------------------------------USER CHECK PROFILE ,EDIT PROFILE AND DELETE AND PROFILE DELETE
@login_required(login_url='/login/')
def profile_view(request):
    return render(request, 'auth/profile.html', {'user': request.user})


@login_required(login_url='/login/')
def profile_edit_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']

        if User.objects.filter(username=username).exclude(pk=request.user.pk).exists():
            messages.error(request, 'Username already taken!')
            return redirect('/profile/edit/')

        request.user.username = username
        request.user.email = email
        request.user.save()
        messages.success(request, 'Profile updated!')
        return redirect('/profile/')

    return render(request, 'auth/profile_edit.html', {'user': request.user})


@login_required(login_url='/login/')
def change_password_view(request):
    if request.method == 'POST':
        old_password = request.POST['old_password']
        new_password1 = request.POST['new_password1']
        new_password2 = request.POST['new_password2']

        if not request.user.check_password(old_password):
            messages.error(request, 'Old password is wrong!')
            return redirect('/change-password/')

        if new_password1 != new_password2:
            messages.error(request, 'Passwords do not match!')
            return redirect('/change-password/')

        request.user.set_password(new_password1)
        request.user.save()
        update_session_auth_hash(request, request.user)  # Session maintain karo
        messages.success(request, 'Password changed!')
        return redirect('/profile/')

    return render(request, 'auth/change_password.html')


@login_required(login_url='/login/')
def delete_account_view(request):
    if request.method == 'POST':
        request.user.delete()
        logout(request)
        messages.success(request, 'Account deleted!')
        return redirect('/register/')

    return render(request, 'auth/delete_account.html')