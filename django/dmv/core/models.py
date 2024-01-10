from django.db import models

class Data(models.Model):
    name = models.CharField(max_length=200)
    text = models.TextField()

class DataUpload(models.Model):
    filename = models.CharField(max_length=100, default='default filename')
    filetype = models.CharField(max_length=100, default='default filetype')
    modelname = models.CharField(max_length=100, default='default model')
    username = models.CharField(max_length=100, default='default user')
    filedate = models.DateTimeField()
    pickledictionary = models.TextField()
    
class Sequence(models.Model):
    filenumber = models.IntegerField()    
