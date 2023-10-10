import math
import os
import json
import requests
import operator
import gevent
from django.http import HttpResponse, JsonResponse
from data.models import *
from nodes.models import *
from django.shortcuts import render
import math
from django.views.decorators.clickjacking import xframe_options_exempt
from smart_city_dashboard.constants import Constants
from huey import crontab
from huey.contrib.djhuey import periodic_task
from types import SimpleNamespace
import datetime
from dateutil.parser import parse
from copy import deepcopy
import pandas as pd
import numpy as np
from datetime import timedelta
from django.utils.timezone import make_aware
from django.db import transaction

from django.core.files import File
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required

def saveVerticalData(request, *args, **kwargs):
    verticalType = request.GET['type']

    if verticalType not in Constants.VTYPE:
        return HttpResponse("Invalid vertical")

    return processSaveVertical(verticalType)


@periodic_task(crontab(minute='*/10'))
def saveVerticals():
    event_spawn = []
    for type in Constants.VTYPE:
        event_spawn.append(gevent.spawn(processSaveVertical,type))
    gevent.wait(event_spawn)


def parseData(data_str, verticalType):
    nan = None
    try:
        data_final = eval(data_str)
        data_final[0] = make_aware(
            datetime.datetime.fromtimestamp(int(data_final[0])))
    except:
        return None

    return data_final


def checkDataExists(LatestNodeId, timestamp, verticalType):
    with transaction.atomic():
        result = Constants.datasetLatest[verticalType].objects.filter(
            id=LatestNodeId, created_at=timestamp)
    if len(result):
        return True
    return False


def processSaveVertical(verticalType):
    headers = {
        'X-M2M-Origin': f"{os.getenv('OM2M_USERNAME','guest')}:{os.getenv('OM2M_PASSWORD','guest')}",
        'Content-Type': 'application/json'
    }
    URL = os.getenv('OM2M_URL','http://onem2m.iiit.ac.in:443/~/in-cse/in-name/')
    with transaction.atomic():
        result = Node.objects.filter(type=verticalType)
    nodes = list(result)

    # if nodes empty then return
    for node in nodes:
        nodeId = node.node_id
        url = f"{URL}" + \
            Constants.om2m_type[verticalType] + '/' + nodeId + "/Data/la"
        response = requests.get(url, headers=headers,
                                verify=False)
        print(('nodeId: {0}\nnode: {1}\nresponse: {2}').format(
            node, nodeId, response))

        if response.status_code != 200:
            continue

            # try:
        data = response.json()
        # except JSONDecodeError:
        #     print("error")
        #     continue

        data_str = data["m2m:cin"]["con"]

        data_final = parseData(data_str, verticalType)
        if data_final == None:
            print("Unexpected data... skipping node")
            continue
            # print(len(data_final))
            # print(data_final)

        latestVerticalId = "VL_10_" + nodeId

        if checkDataExists(latestVerticalId, data_final[0], verticalType):
            print("Data with timestamp {0} already exists... ignoring".format(
                data_final[0]))
            continue

        params = [latestVerticalId, nodeId]

        for x in data_final:
            if type(x) is dict:
                for key, val in x.items():
                    params.append(float(val))
            else:
                params.append(x)

            # air quality has one extra parameter which we want to discard
        params = params[:len(Constants.param_list[verticalType])+3]

        print(params)

        node = Constants.datasetLatest[verticalType](*params)
        with transaction.atomic():
            node.save()

        params[0] = None
        node = Constants.dataset[verticalType](*params)
        with transaction.atomic():
            node.save()
    # fetch all nodes for vertical by querying with type AQ
    # iterate over all nodes and execute below lines
    # In each iteration - append nodeId to url
    # And to DB call

    print("Data saved for vertical "+verticalType)
    return HttpResponse("Data saved for vertical "+verticalType)


def createAllNodes(request, *args, **kwargs):
    docs = '../../docs/'
    fileName = docs + 'all_nodes.json'

    json_data = open(fileName)
    # print("json data=", json_data)
    nodeMasterData = json.load(json_data)  # deserializes it

    for n in nodeMasterData:
        location = Point(n["longitude"], n["latitude"])
        node = Node(n["nodeId"], n["name"], location,
                    n["xcor"],  n["ycor"], n["type"], 't')
        node.save()
    return HttpResponse("Nodes created")


def processAllVerticalDataWithNodes():
    nodes_from_db = Node.objects.filter(visibility=True)
    nodes_list = list(nodes_from_db)

    results = {}

    for type in Constants.VTYPE:
        nodes = [node for node in nodes_list if node.type == type]
        node_ids = [node.node_id for node in nodes]
        data = list(Constants.datasetLatest[type].objects.filter(
            node_id__in=node_ids))
        result = prepareNodeData(nodes, data, type)

        results[Constants.alternate_type[type]] = result
        # print(result,sep="\n")

    return results


def prepareNodeDataGraph(vertical_nodes, vertical_list, verticalType):
    vertical_result = []
    for v_node in vertical_nodes:
        node_vertical_json = {}
        node_vertical_json["node_id"] = v_node.node_id
        node_vertical_json["name"] = v_node.name
        node_vertical_json["latitude"] = v_node.location[1]
        node_vertical_json["longitude"] = v_node.location[0]
        node_vertical_json["type"] = v_node.type
        prepareVerticalDataGraph(vertical_list, v_node, node_vertical_json,
                                 verticalType, vertical_result)  # node_vertical_data =
    return vertical_result


def prepareVerticalDataGraph(data, nodes, node_vertical_json, type, result):

    list_for_node = [
        entry for entry in data if entry.node.node_id == nodes.node_id]

    if len(list_for_node) > 0:
        for entry in list_for_node:
            node_vertical_json["created_at"] = entry.created_at
            node_vertical_json = addNode(type, node_vertical_json, entry)
            result.append(deepcopy(node_vertical_json))


def addNode(type, node_json, vertical_latest):
    for param in Constants.param_list[type]:
        node_json[param] = getattr(vertical_latest, param)
    return node_json


def getGraphData(request, *args, **kwargs):
    # based on node
    # based on vertical
    # based on timestamp
    # print("getGraphData")

    nodesParam = request.GET.get('nodes', None)
    # print("nodes param =", nodesParam)

    verticalType = request.GET.get('type', None)
    # print("vertical type =", verticalType)

    # end, after, now,
    end = request.GET.get('end', None)
    start = request.GET.get('start', None)
    # print("Current timestamp=", datetime.datetime.now())

    interval = request.GET.get('interval', None)
    # print("interval =", interval)

    # Vertical Type validation
    if verticalType is None or verticalType.strip() == '':
        # print("None vertical type")
        return HttpResponse("no type for vertical specified")

    # start, end timestamp validation
    if end is None or start is None:
        # print("end or after is None")
        return HttpResponse("end or start timestamp missing")

    end = parse(end)
    start = parse(start)

    if end < start:
        # print("end < start")
        return HttpResponse("end time cannot be less than start.")

    # Interval validation
    if interval not in Constants.INTERVAL:
        # print("Invalid interval")
        return HttpResponse("invalid interval specified")

    if interval is None:
        interval = "minute"
    # Validation complete

    nodes_for_vertical = Node.objects.filter(type=verticalType)
    if nodesParam is None:
        nodes_from_db = Node.objects.all()
        nodes_list = list(nodes_from_db)
    else:
        nodes_ = nodesParam.split(",")
        nodes_from_db = Node.objects.filter(node_id__in=nodes_)
        nodes_list = list(nodes_from_db)

    results = {}

    if verticalType == 'all':
        for type in Constants.VTYPE:
            nodes = [node for node in nodes_list if node.type == type]
            node_ids = [node.node_id for node in nodes]
            data = list(Constants.dataset[type].objects.filter(node_id__in=node_ids,
                                                               created_at__range=[start, end]).order_by("created_at"))
            result = prepareNodeDataGraph(nodes, data, type)
            results.add(Constants.alternate_type[type], result)

    else:
        node_ids = []
        node_ids_for_vertical = [node.node_id for node in nodes_for_vertical]
        for type in Constants.VTYPE:
            if type == verticalType:
                nodes = [node for node in nodes_list if node.type == type]
                node_ids = [node.node_id for node in nodes]
                data = list(Constants.dataset[type].objects.filter(node_id__in=node_ids,
                                                                   created_at__range=[start, end]).order_by("created_at"))
                parameters = Constants.param_list[type]
                result = prepareNodeDataGraph(nodes, data, verticalType)
                result_key = Constants.alternate_type[type]

        # fields for pandas dataframe
        dfParameters = parameters + ("created_at",)

        if interval == "minute":
            results[result_key] = result

        else:
            new_result = []

            for nodeId in node_ids:
                node_records = [
                    node_record for node_record in result if node_record["node_id"] == nodeId]
                if len(node_records) > 0:
                    # create pandas dataframe with selected fields
                    df = pd.DataFrame(node_records, columns=dfParameters)
                    df['created_at'] = pd.to_datetime(
                        df['created_at'], errors='ignore')
                    # convert created_at to pandas datetime; errors=ignore - ignore parse errors, coerce - set parse errors nan
                    # print("Df=", df)

                    data_daily = []
                    if interval == "hour":
                        data_daily = df.reset_index().set_index('created_at').resample(
                            '1H').mean()  # resample to hour data
                    else:  # interval == "day":
                        data_daily = df.reset_index().set_index(
                            'created_at').resample('1D').mean()  # resample to day data

                    # round values to 3 decimal places
                    data_daily = data_daily.round(decimals=3)

                    # remove filler nan records where hour/day not there in original response
                    data_daily.dropna(
                        subset=['index'], how='any', inplace=True)
                    data_daily.dropna(how='any', inplace=True)
                    data_daily = data_daily.drop(
                        'index', 1)  # column_name: index drop

                    df_dict = data_daily.reset_index().to_dict(
                        orient='index')  # convert dataframe to dict
                    df_vals = list(df_dict.values())

                    for record in df_vals:
                        if len(result) > 0:
                            record['node_id'] = node_records[0]['node_id']
                            record['name'] = node_records[0]['name']
                            record['type'] = verticalType

                    new_result = new_result + df_vals
            results[result_key] = new_result

        results["parameters"] = parameters
        results["nodes"] = node_ids_for_vertical

    return JsonResponse(results)


def getAllVeriticalDataWithNodes(request, *args, **kwargs):
    result = processAllVerticalDataWithNodes()
    return JsonResponse(result)


def loadMapAllVerticals(request, *args, **kwargs):
    result = processAllVerticalDataWithNodes()
    context = {"result": json.dumps(result)}
    response = render(request, 'dashboard/index.html', context)
    response['X-Frame-Options'] = 'ALL'
    return response


def prepareNodeData(vertical_nodes, vertical_list, verticalType):
    vertical_result = []
    for v_node in vertical_nodes:
        node_vertical_json = {}
        node_vertical_json["node_id"] = v_node.node_id
        node_vertical_json["name"] = v_node.name
        node_vertical_json["latitude"] = v_node.location[0] if verticalType=="WN" else v_node.location[1]
        node_vertical_json["longitude"] = v_node.location[1] if verticalType=="WN" else v_node.location[0]
        node_vertical_json["xcor"] = v_node.xcor
        node_vertical_json["ycor"] = v_node.ycor
        node_vertical_json["type"] = v_node.type
        node_vertical_data = prepareVerticalData(
            vertical_list, v_node, node_vertical_json, verticalType)
        if node_vertical_data is not None:
            vertical_result.append(node_vertical_data)

    return vertical_result


def prepareVerticalData(data, nodes, node_vertical_json, type):
    list_for_node = [
        entry for entry in data if entry.node.node_id == nodes.node_id]

    if len(list_for_node) > 0:
        latest = max(list_for_node, key=operator.attrgetter('created_at'))

        units = addUnits(
            latest.__dict__, Constants.units_map[type], *Constants.param_list[type])
        node_vertical_json = addNode(
            type, node_vertical_json, SimpleNamespace(**units))
        return node_vertical_json

    return None


def loadMapWithNodes(request, *args, **kwargs):
    verticalType = request.GET['type']

    nodes_from_db = Node.objects.filter(type=verticalType, visibility=True)
    nodes = list(nodes_from_db)

    node_ids = [node.node_id for node in nodes]
    data_from_db = Constants.dataset[type].objects.filter(node_id__in=node_ids)

    # if aqd_from_db is empty then return
    if len(data_from_db) <= 0:
        return HttpResponse("No vertical data present")

    # can optimize by adding time filter, created_at_gte=60min
    data_list = list(data_from_db)

    result = []
    for node in nodes:
        node_json = {}
        node_json["node_id"] = node.node_id
        node_json["name"] = node.name
        node_json["latitude"] = node.location[1]
        node_json["longitude"] = node.location[0]
        node_json["xcor"] = node.xcor
        node_json["ycor"] = node.ycor
        node_json["type"] = node.type

        # take out aqd objects with particular node_id into an array
        # pick highest value
        data_list_for_node = [
            aqd for aqd in data_list if aqd.node.node_id == node.node_id]

        data_latest = []
        if len(data_list_for_node) > 0:
            data_latest = max(data_list_for_node,
                              key=operator.attrgetter('created_at'))

            node_json = addNode(type, node_json, data_latest)
            result.append(node_json)

    context = {"result": json.dumps(result)}
    return render(request, 'dashboard/index.html', context)


def getVerticalsAverage(request, *args, **kwargs):
    result = processVerticalsAverage()
    return JsonResponse(result)


def processVerticalsAverage():
    nodes_from_db = Node.objects.filter(visibility=True)
    nodes_list = list(nodes_from_db)

    result = {"aq": {"nodes": 0, "name": "Air Quality"},
              "wd": {"nodes": 0, "name": "Water Distribution"},
              "wf": {"nodes": 0, "name": "Water Flow"},
              "we": {"nodes": 0, "name": "Weather Station"},
              "sl": {"nodes": 0, "name": "Solar Energy"},
              "em": {"nodes": 0, "name": "Energy Monitoring"},
              "sr_ac": {"nodes": 0, "name": "Smart Room - Air Conditioning"},
              "sr_aq": {"nodes": 0, "name": "Smart Room - Air Quality"},
              "sr_em": {"nodes": 0, "name": "Smart Room - Energy Monitoring"},
              "sr_oc": {"nodes": 0, "name": "Smart Room - Occupancy"},
              "cm": {"nodes": 0, "name": "Crowd Monitoring"},
              "wn":{"nodes":0,"name":"Wisun"}
              }

    for node in nodes_list:
        result[Constants.alternate_type[node.type]]["nodes"] += 1

    # constants
    for type in Constants.VTYPE:
        data_from_db = Constants.datasetLatest[type].objects.all()
        data_list = list(data_from_db)
        ans = aggregate(result[Constants.alternate_type[type]]["nodes"], data_list,
                        type, *Constants.param_list[type])
        units = addUnits(
            ans, Constants.units_map[type], *Constants.param_list[type])
        result[Constants.alternate_type[type]] = addNode(type, result[Constants.alternate_type[type]],
                                                         SimpleNamespace(**units))

    return result


def getSummaryViewData():
    nodes_from_db = Node.objects.filter(visibility=True)
    nodes_list = list(nodes_from_db)

    result = {"aq": {"nodes": 0, "name": "Air Quality"},
              "wd": {"nodes": 0, "name": "Water Distribution"},
              "wf": {"nodes": 0, "name": "Water Flow"},
              "we": {"nodes": 0, "name": "Weather Station"},
              "sl": {"nodes": 0, "name": "Solar Energy"},
              "em": {"nodes": 0, "name": "Energy Monitoring"},
              "sr": {"nodes": 0, "name": "Smart Room (total)"},
              "sr_ac": {"nodes": 0, "name": "  - Air Conditioning"},
              "sr_aq": {"nodes": 0, "name": "  - Air Quality"},
              "sr_em": {"nodes": 0, "name": "  - Energy Monitoring"},
              "sr_oc": {"nodes": 0, "name": "  - Occupancy"},
              "cm": {"nodes": 0, "name": "Crowd Monitoring"},
              "wn":{"nodes":0, "name":"Wisun"}
              }

    for node in nodes_list:
        result[Constants.alternate_type[node.type]]["nodes"] += 1

    sr_nodes = ["sr_ac", "sr_aq", "sr_em", "sr_oc"]
    for sr_node in sr_nodes:
        result["sr"]["nodes"] += result[sr_node]["nodes"]

    # live average values
    type1 = ['AQ', 'AQ', 'AQ', 'AQ', 'AQ', 'WD', 'SL', 'WF', 'WE']
    atype = [None, None, None, None, None, None, 'sum', 'sum', None]
    node_ids = [None, None, None, None, None, None, None, None, None]
    params = ["temperature", "pm25", "pm10", "relative_humidity", "aqi",
              "compensated_tds_value", 'eac_today', 'total_flow', 'solar_radiation']

    ret = getLiveAverage(type1, params, atype, node_ids)

    for i in range(len(params)):
        result[params[i]] = ret[i]

    # last 24 hours data

    # water usage
    # type1 = 'WF'
    # params = ["created_at", "total_flow"]
    # node_ids = ['WM-WF-PH01-00']

    # ret = getPastDayValues(type1, params, node_ids)

    # result["total_flow"] = ret

    # # solar energy generated
    # type1 = 'SL'
    # params = ["created_at", "eac_today"]

    # ret = getPastDayValues(type1, params)

    # result["eac_today"] = ret

    return result


def getLiveAverage(type1, params, atype, node_ids):
    endDate = datetime.datetime.now()
    startDate = endDate - timedelta(days=2)

    cnt = [0 for p in params]
    ans = [0.0 for p in params]
    for i in range(len(params)):
        if node_ids[i] == None:
            nodes = list(Node.objects.filter(type=type1[i]))
        else:
            nodes = list(Node.objects.filter(
                type=type1[i], node_id=node_ids[i]))
        for node in nodes:
            filter = params[i] + "__isnull"
            data = list(Constants.dataset[type1[i]].objects.filter(node=node.node_id).filter(created_at__range=[make_aware(startDate), make_aware(
                endDate)]).exclude(**{filter: True}).exclude(**{params[i]: math.nan}).exclude(**{params[i]: 0}).order_by("-created_at"))
            try:
                temp = getattr(data[0], params[i])
            except AttributeError and IndexError:
                temp = None

            if temp is not None:
                ans[i] += float(temp)
                cnt[i] += 1

    for i in range(len(params)):
        if cnt[i] and atype[i] == None:
            ans[i] = ans[i]/cnt[i]
        ans[i] = round(ans[i], 0)

    return ans


def getPastDayValues(type1, params, node_ids=None):
    endDate = datetime.datetime.now()
    startDate = endDate - timedelta(days=1)

    if node_ids == None:
        data = list(Constants.dataset[type1].objects.filter
                    (created_at__range=[make_aware(startDate), make_aware(endDate)]).order_by
                    ("created_at").values(*params))
    else:
        data = list(Constants.dataset[type1].objects.filter
                    (node__in=node_ids, created_at__range=[make_aware(startDate), make_aware(endDate)]).order_by
                    ("created_at").values(*params))
    df = pd.DataFrame(data, columns=params)

    df['created_at'] = pd.to_datetime(df['created_at'], errors='ignore')
    df.dropna()
    data_daily = df.reset_index().set_index(
        'created_at').resample('1H').mean().round(decimals=3)
    data_daily = data_daily.drop('index', 1)  # column_name: index drop

    df_dict = data_daily.reset_index().to_dict(
        orient='index')  # convert dataframe to dict
    df_vals = list(df_dict.values())

    return df_vals


def loadHome(request, *args, **kwargs):
    # result = processVerticalsAverage()
    result = getSummaryViewData()
    context = {"result": json.dumps(result)}  # json.dumps(result)
    response = render(request, 'dashboard/home.html', context)
    response['X-Frame-Options'] = 'ALL'
    return response


def addUnits(obj, unit_map, *attributes, **kwargs):
    params = dict.fromkeys(attributes, kwargs.get('start', 0))
    for attr in unit_map:
        # getattr(it, attr['param'])    # print("Value=", value, attr['unit'])
        value = obj[attr['param']]
        if value is None:
            value = "null"
        else:
            if type(value) is str:
                value = float(value)
            value = int(np.round(value, decimals=0))
        params[attr['param']] = str(value) + " " + attr['unit']
    return params


def loadBuilding(request, *args, **kwargs):
    # print("loadbuilding called")
    result = processAllVerticalDataWithNodes()
    context = {"result": json.dumps(result)}  # json.dumps(result)
    return render(request, 'dashboard/building.html', context)


def load3D(request, *args, **kwargs):
    # print("loadbuilding called")
    result = processAllVerticalDataWithNodes()
    context = {"result": json.dumps(result)}  # json.dumps(result)
    return render(request, 'dashboard/3d.html', context)

@xframe_options_exempt
def loadGrafanaView(request, *args, **kwargs):
    context = {}
    return render(request, 'dashboard/grafana.html', context)


def aggregate(n_nodes, iterable, node_type, *attributes, **kwargs):  # **kwargs
    cache = {}
    avgs = dict.fromkeys(attributes, kwargs.get('start', 0))
    cnts = dict.fromkeys(attributes, kwargs.get('start', 0))
    for it in iterable:
        for attr in attributes:
            value = getattr(it, attr)
            key = (node_type, attr)
            atype = 'AVG'
            # if key in cache:
            #    atype = cache[key]
            # else:
            #    atype = AggregationType.objects.filter(node_type=node_type, parameter=attr)[0].aggregation
            #    cache[key] = atype
            if type(value) is str:
                value = float(value)

            if value is not None:
                if atype == 'AVG':
                    avgs[attr] = (avgs[attr]*(cnts[attr]) +
                                  value)/(cnts[attr]+1)
                elif atype == 'MAX':
                    if avgs[attr] != 0.0:
                        avgs[attr] = max(avgs[attr], value)
                    else:
                        avgs[attr] = value
                elif atype == 'MIN':
                    if avgs[attr] != 0.0:
                        avgs[attr] = min(avgs[attr], value)
                    else:
                        avgs[attr] = value
                else:
                    avgs[attr] += value
                cnts[attr] += 1

    return roundParams(avgs)


def roundParams(avgs):
    for param in avgs:
        avgs[param] = round(avgs[param], 3)
    return avgs


def loadPointPicker(request, *args, **kwargs):
    return render(request, 'dashboard/point_picker.html', {})


def get3DConfig(request, *args, **kwargs):
    with open('config.json', 'r') as f:
        nodes = json.load(File(f))
    return HttpResponse(json.dumps(nodes), content_type='application/json')


def save3DConfig(request, *args, **kwargs):
    # Convert request body to JSON
    nodes = json.loads(request.body)

    # Overwrite config file
    with open('config.json', 'w') as f:
        myFile = File(f)
        myFile.write(json.dumps(nodes))

    return HttpResponse(status=200)

@staff_member_required
def wisunDashboard(request):
    nodes = Node.objects.filter(visibility=True)
    nodes = list(nodes)
    results = {}
    nodes = [node for node in nodes if node.type == "WN"]
    node_ids = [node.node_id for node in nodes]
    data = list(Constants.datasetLatest["WN"].objects.filter(
        node_id__in=node_ids))
    result = prepareNodeData(nodes, data, "WN")
    results[Constants.alternate_type["WN"]] = result
    context = {"result": json.dumps(results)}
    return render(request, 'dashboard/wisun.html', context)


@csrf_exempt
def switchOnOff(request, command, id,data):
    print(command, id,data)
    url = "http://onem2m.iiit.ac.in:443/~/in-cse/in-name/AE-WN/"+id+"/Status"
    headers = {
        "X-M2M-Origin": "WisunMon@20:5T&6OnuL1iZ",
        "Content-type": "application/json;ty=4"
    }
    on = {
        "m2m:cin": {
            "con": data,
            "lbl": "",
            "cnf": "text"
        }
    }
    off = {
        "m2m:cin": {
            "con": data,
            "lbl": "",
            "cnf": "text"
        }
    }
    dim = {
        "m2m:cin": {
            "con": '.dim5',
            "lbl": "",
            "cnf": "text"
        }
    }
    if (command == "on"):
        x = requests.post(url, headers=headers, json=on)
        print(url)
        test = x.text
        print(x)
        print(test)
    if (command == "off"):
        x = requests.post(url, headers=headers, json=off)
        test = x.text
        print(x)
        print(test)
    if (command == "dim"):
        x = requests.post(url, headers=headers, json=dim)
        test = x.text
        print(x.text)
    return HttpResponse(x.status_code)

@csrf_exempt
def getAcknowledgement(request,id):
    url = "http://onem2m.iiit.ac.in:443/~/in-cse/in-name/AE-WN/"+id+"/Acknowledge/la"
    headers = {
        "X-M2M-Origin": "guest:guest",
        "Content-type": "application/json"
    }
    response=requests.get(url,headers=headers)
    #print(response.json())
    return HttpResponse(response.json()["m2m:cin"]["con"])
