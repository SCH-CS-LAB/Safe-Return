from django.db import models

# Create your models here.
class LocationData(models.Model):
    name = models.CharField(max_length=50) #마크 이름
    latitude = models.IntegerField() #위도
    longitude = models.IntegerField() #경도

    def __str__(self):
        return self.name