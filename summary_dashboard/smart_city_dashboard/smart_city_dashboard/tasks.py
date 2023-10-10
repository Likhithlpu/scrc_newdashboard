from huey import crontab
from huey.contrib.djhuey import task, periodic_task, db_task
from views import processSaveVertical

# @periodic_task(crontab(minute='*/1'))
# def saveVerticals():
#     print("Huey saveVerticals")
#     processSaveVertical("AQ")
#     processSaveVertical("WD")
#     processSaveVertical("WF")
#     processSaveVertical("WE")
#     processSaveVertical("SL")
#     processSaveVertical("EM")
#     processSaveVertical("SR-AC")
#     processSaveVertical("SR-EM")
#     processSaveVertical("SR-OC")
#     processSaveVertical("SR-AQ")
#     processSaveVertical("CM")
#     processSaveVertical("WN")
#     print("Done")