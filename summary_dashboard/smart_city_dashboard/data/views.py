from django.core.serializers import serialize
from data.models import AirQualityDataLatest, WaterDistributionDataLatest, WaterFlowDataLatest
from nodes.constants import Constants, Vertical_Types
from django.shortcuts import render

# Create your views here.
def db_to_json_aqd():
    pass

def json_to_db_aqd():
    pass

def get_latest_point_of_node(node):
    data_point = None
    if node.type == Vertical_Types.air_quality:
        data_point = AirQualityDataLatest.objects.filter(node = node).first()
    elif node.type == Vertical_Types.water_flow:
        data_point = WaterFlowDataLatest.objects.filter(node = node).first()
    elif node.type == Vertical_Types.water_distribution:
        data_point = WaterDistributionDataLatest.objects.filter(node = node).first()
    
    if data_point is not None:
        data_point = serialize(data_point)
        data_point = data_point[Constants.FIELDS]
        return serialize(data_point)
    else:
        return ""