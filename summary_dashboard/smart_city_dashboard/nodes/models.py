# from django.db import models
from django.contrib.gis.geos import Point
from django.contrib.gis.db import models
# from django.contrib.gis.db import models as geomodels
from location_field.models.spatial import LocationField


# Create your models here.
class NodeLocation(models.Model):
# class NodeLocation(geomodels.Model):
    location_id = models.AutoField(primary_key = True)
    location_name = models.CharField(max_length = 100, default = '-')
    coordinates = LocationField(based_fields=['city'], zoom=18, default=Point(17.44642,78.3481))
    # coordinates = geomodels.PointField(default=Point(78.3481,17.44642))

    def __str__(self):
        return self.location_name
    
    def __unicode__(self):
        return self.location_name
    
    def save(self, *args, **kwargs) :
        data = super(NodeLocation, self).save(*args, **kwargs)
        return data

    class Meta:
        verbose_name_plural="Node Locations"


type_choices = (
    ('AQ', 'AIR QUALITY'),
    ('WF', 'WATER FLOW'),
    ('WD', 'WATER DISTRIBUTION'),
    ('SL', 'SOLAR'),
    ('EM', 'ENERGY MONITORING'),
    ('SR-AQ', 'SMART ROOM - AQ'),
    ('SR-EM', 'SMART ROOM - EM'),
    ('SR-AC', 'SMART ROOM - AC'),
    ('SR-OC', 'SMART ROOM - OC'),
    ('CM', 'CROWD MONITORING'),
    ('WE', 'WEATHER'),
    ('WN','WISUN')
)


class Node(models.Model):
    node_id = models.CharField(max_length=20, primary_key=True)  # node name = nodeid -  merge with node name
    name = models.CharField(max_length=100, default='-')  # node name
    # location = models.ForeignKey(NodeLocation, on_delete = models.CASCADE)
    # coordinates instead of location field
    # location_name is same as node_name ?
    # lat - float
    # long - float
    #latitude = models.FloatField(default=17.44642)
    #longitude = models.FloatField(default=78.3481)
    location = LocationField(default=Point(78.3481, 17.44642))
    xcor = models.FloatField(default=0)
    ycor = models.FloatField(default=0)
    type = models.CharField(choices=type_choices, max_length=30)  # AQ, WF, vertical_id
    visibility = models.BooleanField()
    # getURL = models.URLField(default='-') # not required ?

    def __str__(self):
        return self.name
    
    def __unicode__(self):
        return self.name
    
    def save(self, *args, **kwargs) :
        data = super(Node, self).save(*args, **kwargs)
        return data
    def filter(self, *args, **kwargs) :
        data = super(Node, self).filter(Node, type)
        return data

    class Meta:
        verbose_name_plural="Nodes"


class TypeOfParameter(models.Model):
    param_id = models.AutoField(primary_key = True)
    name = models.CharField(max_length = 30, default = '-')

    def __str__(self):
        return self.name
    
    def __unicode__(self):
        return self.name
    
    def save(self, *args, **kwargs) :
        data = super(TypeOfParameter, self).save(*args, **kwargs)
        return data

class Parameters(models.Model):
    id = models.AutoField(primary_key = True)
    param = models.ForeignKey(TypeOfParameter, on_delete = models.CASCADE)
    node  = models.ForeignKey(Node, on_delete = models.CASCADE)

    def save(self, *args, **kwargs) :
        data = super(Parameters, self).save(*args, **kwargs)
        return data

    class Meta:
        verbose_name_plural="Parameters"
