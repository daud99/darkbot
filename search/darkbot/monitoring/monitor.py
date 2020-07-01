
from search.models import GlobalVar


class Monitor():
    pass

    def __init__(self, type, leakCheck=False):
        self.__type = type
        self.__leakCheck = leakCheck

    def startMonitoring(self):
        GlobalVar.objects.filter(type=self.__type).update(monitoring=True)



    def stopMonitoring(self):
        pass


