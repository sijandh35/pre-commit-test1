from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=200,blank=True,null=True)
    
class Project(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True,related_name='user')
    name = models.CharField(max_length=200,blank=True,null=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='project_category',blank=True,null=True)
    many_category = models.ManyToManyField(Category,related_name='many_category')