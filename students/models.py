from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    GENDER_CHOICES = [
        ('male' , 'Male'),
        ('female' , 'Female'),
        ('other' , 'Other'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE , null=True , blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10 , blank=True)
    gender = models.CharField(max_length=10 , choices=GENDER_CHOICES)
    date_of_birth = models.DateField(null=True , blank=True)
    address = models.TextField(blank=True)
    class_name = models.CharField(max_length=50)
    roll_number = models.CharField(max_length=20 , unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} - {self.roll_number}'
    
class Attendance(models.Model):
    STATUS_CHOICES = [
        ('present' , 'Present'),
        ('absent' , 'Absent'),
        ('late' , 'Late'),
    ]

    student = models.ForeignKey(Student,on_delete=models.CASCADE , related_name= 'attendances')
    date = models.DateField()
    status = models.CharField(max_length=10 , choices=STATUS_CHOICES , default='present')
    remarks = models.CharField(max_length=200 , blank=True)

    class Meta:
        unique_together = ['student' , 'date']

    def __str__(self):
        return f'{self.student.name} - {self.date} - {self.status}'
    
class Result(models.Model):
    GRADE_CHOICES =[
        ('A+' , 'A+'),  ('A', 'A'), ('B+', 'B+'),
        ('B', 'B'), ('C', 'C'), ('D', 'D'), ('F', 'F'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='results')
    subject = models.CharField(max_length=100)
    marks_obtained = models.IntegerField()
    total_marks = models.IntegerField()
    grade = models.CharField(max_length=5, choices=GRADE_CHOICES)
    exam_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.name} - {self.subject} - {self.grade}"