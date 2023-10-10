
import os
import json
from pathlib import Path

FILE_DIR = Path(__file__).resolve().parent.parent.parent

def read_data(fileName):


    pass


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_city_dashboard.settings')
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
    from nodes.models import Node, NodeLocation, TypeOfParameter, Parameters    

    # delete all current nodes present
    # Node.objects.all().delete()
    # NodeLocation.objects.all().delete()
    # TypeOfParameter.objects.all().delete()
    # Parameters.objects.all().delete()
    print("All Nodes Deleted")

    # Reading Data
    from csv import reader
    from django.contrib.gis.geos import Point
    # fileName = docs + 'all_nodes.json'
    fileName = FILE_DIR / "docs/all_nodes.json"

    json_data = open(fileName)
    print("json data=", json_data)
    data1 = json.load(json_data)  # deserializes it
    # all_nodes = json.dumps(data1)  # json formatted string

    for n in data1:
        #node = Node("AQ-MG00-00",78.34605, 17.44509,"AQ-MG00-00","AQ")
        node, created = Node.objects.get_or_create(node_id=n["nodeId"],defaults={'name':n["name"], 'location':Point(n["latitude"], n["longitude"]), 'xcor':n["xcor"], 'ycor':n["ycor"], 'type':n["type"],'visibility':True})
        print("node =", n, created)
        # node.save()

    json_data.close()

    # with open(fileName, 'r') as ptr:
        # csv_reader = reader(ptr, delimiter = '\t')
        # for record in csv_reader:
        #     x_coor = float(record[3])
        #     y_coor = float(record[2])
        #     type = 'WF'
        #
        #     # check if location already present else create new one
        #     obj, created = NodeLocation.objects.get_or_create(\
        #         coordinates = Point(x_coor, y_coor),
        #         location_name = record[0].strip()
        #     )
        #
        #     curr = Node(\
        #         name = record[1].strip(),
        #         type = type,
        #         getURL = record[4].strip(),
        #         location = obj
        #     )
        #     curr.save()
        #
        #     params = record[5][1:-1]
        #     params =  [x.strip()[1:-1] for x in params.split(',')]
        #     param_objs = []
        #     for param in params:
        #         obj, created = TypeOfParameter.objects.get_or_create(name = param)
        #         curr_param = Parameters(\
        #             param = obj,
        #             node = curr
        #         )
        #         curr_param.save()
            

            
    print("Reading and adding Done")






if __name__ == '__main__':
    main()