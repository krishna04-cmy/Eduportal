from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Post(models.Model):
    STATUS_CHOICES = [
        ('draft' , 'Draft'),
        ('published' , 'Published'),
    ]

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL , null=True , blank=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    status = models.CharField(max_length=20 , choices=STATUS_CHOICES , default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    post = models.ForeignKey(Post , on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author.username} - {self.post.title}'