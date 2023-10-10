from data.models import *
from django.contrib import admin
from django.contrib.admin.decorators import register


# Register your models here.

@register(AirQualityData)
class AirQualityDataAdmin(admin.ModelAdmin):
    list_filter = ['created_at', 'node']
    list_display = [field.name for field in AirQualityData._meta.get_fields()]

@register(WaterFlowData)
class WaterFlowDataAdmin(admin.ModelAdmin):
    list_filter = ['created_at', 'node']
    list_display = [field.name for field in WaterFlowData._meta.get_fields()]

@register(WaterDistributionData)
class WaterDistributionDataAdmin(admin.ModelAdmin):
    list_filter = ['created_at', 'node']
    list_display = [field.name for field in WaterDistributionData._meta.get_fields()]

@register(WeatherData)
class WetherData(admin.ModelAdmin):
    list_filter = ['created_at', 'node']
    list_display = [field.name for field in WeatherData._meta.get_fields()]

@register(SolarData)
class SolarData(admin.ModelAdmin):
    list_filter = ['created_at', 'node']
    list_display = [field.name for field in SolarData._meta.get_fields()]

@register(EnergyMonitoringData)
class EnergyMonitoringData(admin.ModelAdmin):
    list_filter = ['created_at', 'node']
    list_display = [field.name for field in EnergyMonitoringData._meta.get_fields()]

@register(CrowdMonitoringData)
class CrowdMonitoringData(admin.ModelAdmin):
    list_filter = ['created_at', 'node']
    list_display = [field.name for field in CrowdMonitoringData._meta.get_fields()]

@register(SmartroomACData)
class SmartroomACData(admin.ModelAdmin):
    list_filter = ['created_at', 'node']
    list_display = [field.name for field in SmartroomACData._meta.get_fields()]

@register(SmartroomEMData)
class SmartroomEMData(admin.ModelAdmin):
    list_filter = ['created_at', 'node']
    list_display = [field.name for field in SmartroomEMData._meta.get_fields()]

@register(SmartroomOCData)
class SmartroomOCData(admin.ModelAdmin):
    list_filter = ['created_at', 'node']
    list_display = [field.name for field in SmartroomOCData._meta.get_fields()]

@register(SmartroomAQData)
class SmartroomAQData(admin.ModelAdmin):
    list_filter = ['created_at', 'node']
    list_display = [field.name for field in SmartroomAQData._meta.get_fields()]

@register(AirQualityDataLatest)
class AirQualityDataLatestAdmin(admin.ModelAdmin):
    list_filter = ['created_at', 'id', 'node']
    list_display = [field.name for field in AirQualityDataLatest._meta.get_fields()]

@register(WaterFlowDataLatest)
class WaterFlowDataLatestAdmin(admin.ModelAdmin):
    list_filter = ['created_at', 'id', 'node']
    list_display = [field.name for field in WaterFlowDataLatest._meta.get_fields()]

@register(WaterDistributionDataLatest)
class WaterDistributionDataLatestAdmin(admin.ModelAdmin):
    list_filter = ['created_at', 'id', 'node']
    list_display = [field.name for field in WaterDistributionDataLatest._meta.get_fields()]

@register(WeatherDataLatest)
class WetherDataLatest(admin.ModelAdmin):
    list_filter = ['created_at', 'id', 'node']
    list_display = [field.name for field in WeatherDataLatest._meta.get_fields()]

@register(SolarDataLatest)
class SolarDataLatest(admin.ModelAdmin):
    list_filter = ['created_at', 'id', 'node']
    list_display = [field.name for field in SolarDataLatest._meta.get_fields()]

@register(EnergyMonitoringDataLatest)
class EnergyMonitoringDataLatest(admin.ModelAdmin):
    list_filter = ['created_at', 'id', 'node']
    list_display = [field.name for field in EnergyMonitoringDataLatest._meta.get_fields()]

@register(CrowdMonitoringDataLatest)
class CrowdMonitoringDataLatest(admin.ModelAdmin):
    list_filter = ['created_at', 'id', 'node']
    list_display = [field.name for field in CrowdMonitoringDataLatest._meta.get_fields()]

@register(SmartroomACDataLatest)
class SmartroomACDataLatest(admin.ModelAdmin):
    list_filter = ['created_at', 'id', 'node']
    list_display = [field.name for field in SmartroomACDataLatest._meta.get_fields()]

@register(SmartroomEMDataLatest)
class SmartroomEMDataLatest(admin.ModelAdmin):
    list_filter = ['created_at', 'id', 'node']
    list_display = [field.name for field in SmartroomEMDataLatest._meta.get_fields()]

@register(SmartroomOCDataLatest)
class SmartroomOCDataLatest(admin.ModelAdmin):
    list_filter = ['created_at', 'id', 'node']
    list_display = [field.name for field in SmartroomOCDataLatest._meta.get_fields()]

@register(SmartroomAQDataLatest)
class SmartroomAQDataLatest(admin.ModelAdmin):
    list_filter = ['created_at', 'id', 'node']
    list_display = [field.name for field in SmartroomAQDataLatest._meta.get_fields()]

@register(WisunNodesData)
class WisunNodesData(admin.ModelAdmin):
    list_filter=['created_at','id','node']
    list_display=[field.name for field in WisunNodesData._meta.get_fields()]
@register(WisunNodesDataLatest)
class WisunNodesDataLatest(admin.ModelAdmin):
    list_filter=['created_at','id','node']
    list_display=[field.name for field in WisunNodesDataLatest._meta.get_fields()]

# admin.site.register(WisunNodesData)
# admin.site.register(WisunNodesDataLatest)