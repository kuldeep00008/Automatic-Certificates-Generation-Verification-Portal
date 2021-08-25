from django.db import models

# Create your models here.
class details(models.Model):
    name = models.CharField(max_length=30)
    organization = models.CharField(max_length=50)
    certification = models.CharField(max_length=50)
    mail = models.EmailField(max_length=254)
    uid = models.CharField(max_length=70, default=000000)

    def __str__(self):
        return self.name

    

