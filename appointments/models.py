from django.db import models
from django.contrib.auth.models import User

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending' , 'Pending'),
        ('approved' , 'Approved'),
        ('rejected' , 'Rejected'),
    ]

    student = models.ForeignKey(User, on_delete=models.CASCADE , related_name='appointments')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20 , choices=STATUS_CHOICES , default='pending') 
    admin_note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.student.username} - {self.title} - {self.date}'