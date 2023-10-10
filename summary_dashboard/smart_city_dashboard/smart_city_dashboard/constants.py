from data.models import *

class Constants:
    INTERVAL = [None, "minute", "hour", "day"]
    FIELDS = 'fields'
    NAME = 'name'
    LOCATION_NAME = 'location_name'
    COORDS = 'coordinates'
    DATA = 'data'
    VTYPE = ['WN', 'AQ', 'WF', 'WD', 'SL', 'EM', 'SR-AQ', 'SR-EM', 'SR-AC', 'SR-OC', 'CM', 'WE']
    
    om2m_type = {'AQ': 'AE-AQ', 'WF': 'AE-WM/WM-WF', 'WD': 'AE-WM/WM-WD',
        'SL': 'AE-SL', 'EM': 'AE-EM', 'SR-AQ': 'AE-SR/SR-AQ',
        'SR-EM': 'AE-SR/SR-EM', 'SR-AC': 'AE-SR/SR-AC', 'SR-OC': 'AE-SR/SR-OC', 
        'CM': 'AE-CM', 'WE': 'AE-WE','WN':'AE-WN'}

    alternate_type = {'AQ': 'aq', 'WF': 'wf', 'WD': 'wd', 'SL': 'sl', 'EM': 'em', 
        'SR-AQ': 'sr_aq', 'SR-EM': 'sr_em', 'SR-AC': 'sr_ac', 'SR-OC': 'sr_oc', 
        'CM': 'cm', 'WE': 'we','WN':'wn'}
    
    dataset = {'AQ': AirQualityData, 'WF': WaterFlowData, 'WD': WaterDistributionData, 
        'SL': SolarData, 'EM': EnergyMonitoringData, 'SR-AQ': SmartroomAQData, 
        'SR-EM': SmartroomEMData, 'SR-AC': SmartroomACData, 'SR-OC': SmartroomOCData, 
        'CM': CrowdMonitoringData, 'WE': WeatherData,'WN':WisunNodesData}

    datasetLatest = {'AQ': AirQualityDataLatest, 'WF': WaterFlowDataLatest, 'WD': WaterDistributionDataLatest, 
        'SL': SolarDataLatest, 'EM': EnergyMonitoringDataLatest, 'SR-AQ': SmartroomAQDataLatest, 
        'SR-EM': SmartroomEMDataLatest, 'SR-AC': SmartroomACDataLatest, 'SR-OC': SmartroomOCDataLatest, 
        'CM': CrowdMonitoringDataLatest, 'WE': WeatherDataLatest,'WN':WisunNodesDataLatest}

    aq_param_units_map = [{'param': 'pm25', 'unit': 'ppm'}, {'param': 'pm10', 'unit': 'ppm'},
                          {'param': 'temperature', 'unit': '°C'},
                          {'param': 'relative_humidity', 'unit': '%'}, {'param': 'co', 'unit': 'ppm'},
                          {'param': 'no2', 'unit': 'ppm'},
                          {'param': 'nh3', 'unit': 'ppm'}, {'param': 'aqi', 'unit': ''},
                          {'param': 'aql', 'unit': ''}, {'param': 'aqi_mp', 'unit': ''}]
    wn_param_units_map=[{'param':'rssi','unit':''},{'param':'latency','unit':''},{'param':'data_rate','unit':''},
                        {'param':'packet_size','unit':''},{'param':'rsl_in','unit':''},
                        {'param':'etx','unit':''},{'param':'rpl_rank','unit':''},{'param':'mac_tx_failed_count','unit':''},
                        {'param':'mac_tx_count','unit':''}]

    wd_param_units_map = [{'param': 'temperature', 'unit': '°C'}, {'param': 'tds_voltage', 'unit': 'V'},
                          {'param': 'uncompensated_tds_value', 'unit': 'ppm'},
                          {'param': 'compensated_tds_value', 'unit': 'ppm'},
                          {'param': 'water_level', 'unit': 'cm'}, {'param': 'ph', 'unit': ''},
                          {'param': 'turbidity', 'unit': 'NTU'}]

    wf_param_units_map = [{'param': 'flowrate', 'unit': 'm³/h'}, {'param': 'total_flow', 'unit': 'm³'},
                          {'param': 'pressure', 'unit': 'P'}, {'param': 'pressure_voltage', 'unit': 'V'}]

    we_param_units_map = [{'param': 'solar_radiation', 'unit': 'W/m²'}, {'param': 'temperature', 'unit': '°C'},
                          {'param': 'relative_humidity', 'unit': '%'}, {'param': 'wind_direction', 'unit': ''},
                          {'param': 'wind_speed', 'unit': 'm/s'}, {'param': 'gust_speed', 'unit': 'm/s'},
                          {'param': 'dew_point', 'unit': ''}, {'param': 'battery_dc_voltage', 'unit': 'V'},
                          {'param': 'rain', 'unit': ''}, {'param': 'pressure', 'unit': 'P'}]

    sl_param_units_map = [{'param': 'eac_today', 'unit': ''}, {'param': 'eac_total', 'unit': ''},
                          {'param': 'active_power', 'unit': 'KW'}, {'param': 'voltage_rs', 'unit': 'V'},
                          {'param': 'voltage_st', 'unit': 'V'}, {'param': 'voltage_tr', 'unit': 'V'},
                          {'param': 'frequency', 'unit': 'Hz'}, {'param': 'power_factor', 'unit': ''},
                          {'param': 'voltage1', 'unit': 'V'}, {'param': 'current1', 'unit': 'A'},
                          {'param': 'power1', 'unit': 'W'},
                          {'param': 'voltage2', 'unit': 'V'}, {'param': 'current2', 'unit': 'A'},
                          {'param': 'power3', 'unit': 'W'},
                          {'param': 'pv1_voltage', 'unit': 'V'}, {'param': 'pv1_current', 'unit': 'A'},
                          {'param': 'pv1_power', 'unit': 'W'},
                          {'param': 'pv2_voltage', 'unit': 'V'}, {'param': 'pv2_current', 'unit': 'A'},
                          {'param': 'pv2_power', 'unit': 'W'},
                          {'param': 'pv3_voltage', 'unit': 'V'}, {'param': 'pv3_current', 'unit': 'A'},
                          {'param': 'pv3_power', 'unit': 'W'},
                          {'param': 'pv4_voltage', 'unit': 'V'}, {'param': 'pv4_current', 'unit': 'A'},
                          {'param': 'pv4_power', 'unit': 'W'},
                          {'param': 'pv5_voltage', 'unit': 'V'}, {'param': 'pv5_current', 'unit': 'A'},
                          {'param': 'pv5_power', 'unit': 'W'},
                          {'param': 'pv6_voltage', 'unit': 'V'}, {'param': 'pv6_current', 'unit': 'A'},
                          {'param': 'pv6_power', 'unit': 'W'}]

    em_param_units_map = [{'param': 'rssi', 'unit': ''}, {'param': 'r_current', 'unit': 'A'},
                          {'param': 'y_current', 'unit': 'A'}, {'param': 'b_current', 'unit': 'A'},
                          {'param': 'r_voltage', 'unit': 'V'}, {'param': 'y_voltage', 'unit': 'V'},
                          {'param': 'b_voltage', 'unit': 'V'}, {'param': 'frequency', 'unit': 'Hz'},
                          {'param': 'apparent_power', 'unit': 'kW'}, {'param': 'real_power', 'unit': 'kW'},
                          {'param': 'energy_consumption', 'unit': ''}, {'param': 'reactive_energy_lead', 'unit': ''},
                          {'param': 'reactive_energy_lag', 'unit': '%'},
                          {'param': 'total_energy_consumption', 'unit': ''}]

    cm_param_units_map = [{'param': 'current_people_count', 'unit': ''},
                          {'param': 'no_of_safe_distance_violations', 'unit': ''},
                          {'param': 'no_of_mask_violations', 'unit': ''}, {'param': 'timestamp_start', 'unit': ''},
                          {'param': 'timestamp_end', 'unit': ''}]

    srac_param_units_map = [{'param': 'room_temp', 'unit': '°C'}, {'param': 'temp_adjust', 'unit': '°C'},
                            {'param': 'start_stop_status', 'unit': '°C'}, {'param': 'alarm', 'unit': '%'},
                            {'param': 'malfunction_code', 'unit': '%'}, {'param': 'air_con_mode_status', 'unit': '%'},
                            {'param': 'air_flow_rate_status', 'unit': '%'}, {'param': 'filter_sign', 'unit': '%'},
                            {'param': 'gas_total_power', 'unit': '%'}, {'param': 'elec_total_power', 'unit': '%'},
                            {'param': 'air_direction_status', 'unit': '%'},
                            {'param': 'forced_thermo_off_status', 'unit': '%'},
                            {'param': 'energy_efficiency_status', 'unit': '%'},
                            {'param': 'compressor_status', 'unit': '%'},
                            {'param': 'indoor_fan_status', 'unit': '%'}, {'param': 'heater_status', 'unit': '%'}]

    sraq_param_units_map = [{'param': 'co2', 'unit': 'ppm'}, {'param': 'temperature', 'unit': '°C'},
                            {'param': 'relative_humidity', 'unit': '%'}]

    srem_param_units_map = [{'param': 'energy', 'unit': 'kJ'}, {'param': 'power', 'unit': 'kW'},
                            {'param': 'current', 'unit': 'A'}]

    sroc_param_units_map = [{'param': 'occupancy1', 'unit': ''}, {'param': 'occupancy2', 'unit': ''},
                            {'param': 'occupancy3', 'unit': ''}, {'param': 'occupancy4', 'unit': ''},
                            {'param': 'temperature', 'unit': '°C'}, {'param': 'relative_humidity', 'unit': '%'}]

    units_map = {'AQ': aq_param_units_map, 'WF': wf_param_units_map, 'WD': wd_param_units_map, 
        'SL': sl_param_units_map, 'EM': em_param_units_map, 'SR-AQ': sraq_param_units_map, 
        'SR-EM': srem_param_units_map, 'SR-AC': srac_param_units_map, 'SR-OC': sroc_param_units_map, 
        'CM': cm_param_units_map, 'WE': we_param_units_map,'WN':wn_param_units_map}

    aq_param_list = ('pm25', 'pm10', 'temperature', 'relative_humidity', 'co', 'no2', 'nh3', 'aqi', 'aql', 'aqi_mp')
    wn_param_list=('rssi','latency','data_rate','packet_size','rsl_in','etx',
                   'rpl_rank','mac_tx_failed_count','mac_tx_count')
    wd_param_list = (
        'temperature', 'tds_voltage', 'uncompensated_tds_value', 'compensated_tds_value', 'water_level', 'ph',
        'turbidity')
    wf_param_list = ('flowrate', 'total_flow', 'pressure', 'pressure_voltage')
    we_param_list = (
        'solar_radiation', 'temperature', 'relative_humidity', 'wind_direction', 'wind_speed', 'gust_speed',
        'dew_point',
        'battery_dc_voltage', 'rain', 'pressure')
    sl_param_list = (
        'eac_today', 'eac_total', 'active_power', 'voltage_rs', 'voltage_st', 'voltage_tr', 'frequency', 'power_factor',
        'voltage1', 'current1', 'power1', 'voltage2', 'current2', 'power2', 'voltage3', 'current3', 'power3',
        'pv1_voltage',
        'pv1_current', 'pv1_power', 'pv2_voltage', 'pv2_current', 'pv2_power', 'pv3_voltage', 'pv3_current',
        'pv3_power',
        'pv4_voltage', 'pv4_current', 'pv4_power', 'pv5_voltage', 'pv5_current', 'pv5_power', 'pv6_voltage',
        'pv6_current',
        'pv6_power')
    em_param_list = (
        'rssi', 'r_current', 'y_current', 'b_current', 'r_voltage', 'y_voltage', 'b_voltage', 'power_factor',
        'frequency',
        'apparent_power', 'real_power', 'energy_consumption', 'reactive_energy_lead', 'reactive_energy_lag',
        'total_energy_consumption')
    cm_param_list = (
        'current_people_count', 'no_of_safe_distance_violations', 'no_of_mask_violations', 'timestamp_start',
        'timestamp_end')
    srac_param_list = (
        'room_temp', 'temp_adjust', 'start_stop_status', 'alarm', 'malfunction_code', 'air_con_mode_status',
        'air_flow_rate_status', 'filter_sign', 'gas_total_power', 'elec_total_power', 'air_direction_status',
        'forced_thermo_off_status', 'energy_efficiency_status', 'compressor_status', 'indoor_fan_status',
        'heater_status')
    sraq_param_list = ('co2', 'temperature', 'relative_humidity')
    srem_param_list = ('energy', 'power', 'current')
    sroc_param_list = ('occupancy1', 'occupancy2', 'occupancy3', 'occupancy4', 'temperature', 'relative_humidity')

    param_list = {'AQ': aq_param_list, 'WF': wf_param_list, 'WD': wd_param_list, 
        'SL': sl_param_list, 'EM': em_param_list, 'SR-AQ': sraq_param_list, 
        'SR-EM': srem_param_list, 'SR-AC': srac_param_list, 'SR-OC': sroc_param_list, 
        'CM': cm_param_list, 'WE': we_param_list,'WN':wn_param_list}