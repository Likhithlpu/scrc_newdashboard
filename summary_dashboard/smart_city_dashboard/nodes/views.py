from data.views import get_latest_point_of_node
from nodes.constants import Constants, Vertical_Types
from django.shortcuts import render
from .models import Node
from django.core.serializers import serialize
from django.forms.models import model_to_dict
import json



FIELDS = 'fields'
NAME = 'name'
NODEID = 'nodeID'
COORDS = 'coordinates'
COORD = 'coordinate'
LOCATION = 'location'
NODES = 'nodes'


def get_coord_from_location(location):
    location_serialized = model_to_dict(location)
    fields = location_serialized
    print(fields[Constants.COORDS][0])
    coords = [fields[Constants.COORDS][1], fields[Constants.COORDS][0]]
    location_name = fields[Constants.LOCATION_NAME]
    return location_name, coords

def get_data_point(node):
    node_serialized = model_to_dict(node)
    # print(node_serialized)
    fields = node_serialized
    loc_name, coords = get_coord_from_location(node.location)
    node_data = get_latest_point_of_node(node)
    return { 
        Constants.NAME: fields[Constants.NAME],
        Constants.COORDS: coords,
        Constants.LOCATION_NAME: loc_name,
        Constants.DATA: node_data,
    }



# # Create your views here.
def load_map_view(request):
    nodes_from_db = Node.objects.all()
    # nodes_serialized = serialize('json', nodes_from_db)
    final_data = {
        Vertical_Types.air_quality: [],
        Vertical_Types.water_flow: [],
        Vertical_Types.water_distribution: [],
    }
    
    for node in nodes_from_db:
        if node.type in final_data:
            # print(node)
            curr_data = get_data_point(node)
            # print(final_data)
            final_data[node.type].append(curr_data)        

    context = {
        Vertical_Types.air_quality: json.dumps(final_data[Vertical_Types.air_quality]),
        Vertical_Types.water_flow: json.dumps(final_data[Vertical_Types.water_flow]),
        Vertical_Types.water_distribution: json.dumps(final_data[Vertical_Types.water_distribution]),
    }
    return render(request, 'dashboard/index.html', context)
