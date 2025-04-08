from django.db import models

# Create your models here.
class userregistermodel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phoneno = models.IntegerField()
    status = models.CharField(max_length=100)

    def __str__(self):
        return self.email
    
    class Meta:
        db_table = "userregistermodel"

class userimagepredictionmodel(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=100)
    emotion = models.CharField(max_length=100)
    filename = models.CharField(max_length=100)
    file = models.FileField(upload_to='files/')

    def __str__(self):
        return self.email
    
    class Meta:
        db_table = 'userimagepredictionmodel'