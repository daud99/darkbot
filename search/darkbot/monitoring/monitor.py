
from search.models import GlobalVar, MonitorAsset
from search.api import views


class Monitor():

    def __init__(self, type, leakCheck=False):
        self.__type = type
        self.__leakCheck = leakCheck

    def startMonitoring(self):
        GlobalVar.objects.filter(type=self.__type).update(monitoring=True)
        assets = MonitorAsset.objects.filter(asset_type=self.__type).count()
        if assets == 0:
            print("No asset to monitor")
            self.stopMonitoring()
        else:
            assets = MonitorAsset.objects.filter(asset_type=self.__type)
            obj = {"type": self.__type, "wildcard": 'false', "regex": 'false'}
            for each in assets:
                obj["query"] = each.asset
                records_from_db = views.getRecordsFromDB(obj)
                print("records_from_db")
                print(records_from_db)
                # print(each)
                # print(each.asset_type)
                # print(each.asset)


    def stopMonitoring(self):
        GlobalVar.objects.filter(type=self.__type).update(monitoring=False)


