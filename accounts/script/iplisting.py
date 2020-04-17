from accounts.models import IpWhiteList, User
def addip(ipaddress,email):
    print('addip function is called')
    print(ipaddress)
    print('above is ipaddress i receive')
    user = User.objects.get(email__iexact=email)
    newip = IpWhiteList()
    newip.ipaddress = ipaddress
    newip.user = user
    newip.save()
    print('check database to confirm ip address is added or not')