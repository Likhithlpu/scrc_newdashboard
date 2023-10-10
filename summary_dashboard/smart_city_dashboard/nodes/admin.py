# from django.contrib import admin
# from nodes.forms import NodeLocationForm
from csv import list_dialects
from django.contrib.admin.decorators import register
from django.contrib import admin

# from django.contrib.gis import admin

# Register your models here.
from .models import *

@register(Node)
class NodeAdmin(admin.ModelAdmin):
    fields = ('node_id', 'name', 'location', ('xcor', 'ycor'), 'type', 'visibility')
    list_filter = ('type', 'visibility', 'name')
    list_display = ('node_id', 'name', 'type', 'visibility')

# @register(AggregationType)
# class AggregationTypeAdmin(admin.ModelAdmin):
#     list_display = ('node_type', 'parameter', 'aggregation')
#     list_filter = ('node_type', 'aggregation')
