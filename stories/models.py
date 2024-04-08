from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User

class Editor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    bio = models.TextField()
    photo = models.ImageField(upload_to='editors/', null=True, blank=True)

    def __str__(self):
        return self.name
    
class Subcategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Stories(models.Model): 
    CATEGORY_CHOICES = [
        ('personal', 'Personal'),
        ('social', 'Social'),
        ('professional', 'Professional'),
    ]

    image = models.ImageField(upload_to='stories/', null=True, blank=True)  
    title = models.CharField(max_length=200)
    content = models.TextField()
    excerpt = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.CharField(max_length=15, choices=CATEGORY_CHOICES, default='personal')
    subcategory = models.ForeignKey(Subcategory, on_delete=models.SET_NULL, null=True, blank=True)
    editor = models.ForeignKey(Editor, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

class ReadingList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    story = models.ForeignKey(Stories, on_delete=models.CASCADE)
