from data.models import WaterFlowData
from requests import get
import json


def checkFloat(strg):
    try:
        return(round(float(strg), 2))
    except:
        return(-1.0)

def map_data_aq(data):
    pass

def get_db_row_from_data_aq(data):
    pass

def get_latest_db_row_from_data_aq(data):
    pass

def map_data_wd(data):
    pass

def get_db_row_from_data_wd(data):
    pass

def get_latest_db_row_from_data_wd(data):
    pass

def map_data_wf(data):
    pass

def get_db_row_from_data_wf(data):
    return WaterFlowData(
        created_at = data['created_at'],
    )
    pass

def get_latest_db_row_from_data_wf(data):
    pass

def map_data(data, node):
    data = json.loads(data)
    data_point_db = None
    data_latest_point_db = None
    if node.type == 'AQ':
        data_point = map_data_aq(data)
        data_point_db = get_db_row_from_data_aq(data_point) 
        data_latest_point_db = get_latest_db_row_from_data_aq(data_point) 
    elif node.type == 'WF':
        data_point = map_data_wf(data)
        data_point_db = get_db_row_from_data_wf(data_point) 
        data_latest_point_db = get_latest_db_row_from_data_wf(data_point) 
    elif node.type == 'WD':
        data_point = map_data_wd(data)
        data_point_db = get_db_row_from_data_wd(data_point) 
        data_latest_point_db = get_latest_db_row_from_data_wd(data_point) 
    return data_point_db, data_latest_point_db        


def api_call(node):
    data_db = None
    data_db_latest = None
    try:
        headers={
            'X-M2M-Origin':'guest:guest',
            'Content-Type':'application/json'
        }
        response = get(node.getURL, headers=headers)
        print(response.status_code)

        default = {}
        if not response.status_code == '200':
            return data_db, data_db_latest 
        
        data_db, data_db_latest = map_data(response.text, node)

    except Exception as e:
        print(e)

    return data_db, data_db_latest
    # pass