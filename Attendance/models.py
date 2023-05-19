from django.db import models

# Create your models here.
class Attendance(models.Model):
    studentId = models.IntegerField(null=True,blank=True)
    studentName = models.CharField(max_length=50,null=True,blank=True)
    studentYear = models.IntegerField(null=True,blank=True)
    studentSection = models.IntegerField(null=True,blank=True)
    studentImage = models.ImageField(upload_to='photos/%y/%m/%d',null=True,blank=True)
    
    def __str__(self):
        return self.studentName
    
    

 

