from requests import api
from .models import AirQualityData, AirQualityDataLatest, WaterDistributionDataLatest, WaterFlowData, WaterDistributionData, WaterFlowDataLatest
from nodes.models import Node

from huey import crontab
from huey.contrib.djhuey import task, periodic_task, db_task
from nodes.utils import api_call

def getDataOfNode(node):
    type = node.type
    url = node.getURL
    print(type)
    data, dataLatest = api_call(node)
    return data, dataLatest

# @periodic_task(crontab(minute='*/1'))
def getData():
    nodes = Node.objects.all()
    for elem in nodes:
        data, dataLatest = getDataOfNode(elem)
        if data is not None:
            data.save()
            dataLatest.save()
        if elem.type == 'AQ':
            if AirQualityDataLatest.objects.filter(node = elem).count() >= 2:
                AirQualityDataLatest.objects.filter(node = elem).first().delete()
        elif elem.type == 'WF':
            if WaterFlowDataLatest.objects.filter(node = elem).count() >= 2:
                WaterFlowDataLatest.objects.filter(node = elem).first().delete()
        elif elem.type == 'WF':
            if WaterDistributionDataLatest.objects.filter(node = elem).count >= 2:
                WaterDistributionDataLatest.objects.filter(node = elem).first().delete()
        



if __name__ == '__main__':
    getData()