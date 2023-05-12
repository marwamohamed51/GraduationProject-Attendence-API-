from django.db import models

# Create your models here.

dept =(
    ('it','it'),
    ('cs','cs'),
)
class Student(models.Model):
    StudentName = models.CharField(max_length=50,blank=True,null=True),
    StudentSection = models.IntegerField(max_length=15,blank=True,null=True),
    StudentDrpt = models.CharField(max_length=2,choices=dept,blank=True,null=True),
    

    def __str__(self):
        return self.StudentName

class Attended(models.Model):
    Name = models.CharField(max_length=50,blank=True,null=True),
    Section = models.IntegerField(max_length=15,blank=True,null=True),
 

