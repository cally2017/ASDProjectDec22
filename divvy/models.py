from django.db import models

class Bikeshare(models.Model):
    start_time = models.DateTimeField(("start_time"))
    end_time = models.DateTimeField(("end_time"))
    tripduration = models.IntegerField(("tripduration"))
    from_station_id = models.CharField(("from_station_id"), max_length=10)
    from_station_name = models.CharField(("from_station_name"), max_length=255)
    to_station_id = models.CharField(("to_station_id"), max_length=10)
    to_station_name = models.CharField(("to_station_name"), max_length=255)
    usertype = models.CharField(("usertype"), max_length=50)
    from_Latitude = models.FloatField(("from_Latitude"))
    from_Longitude = models.FloatField(("from_Longitude"))
    from_Location = models.CharField(("from_Location"), max_length=150)
    to_Latitude = models.FloatField(("to_Latitude"))
    to_Longitude = models.FloatField(("to_Longitude"))
    to_Location = models.CharField(("to_Location"), max_length=150)

