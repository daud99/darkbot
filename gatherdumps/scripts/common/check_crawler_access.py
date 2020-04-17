from gatherdumps.models import CrawlerAccess, Crawler_Breaker
def check_start_permission(access_identity):
    check = False
    try:
        access_object = CrawlerAccess.objects.get(Access_identity__exact=access_identity)
        check = access_object.authorize_access
    except Exception as e:
        return False
    else:
        return check
    return check

def check_cancel_permission(access_identity):
    check = False
    try:
        access_object = CrawlerAccess.objects.get(Access_identity__exact=access_identity)
        check = access_object.authorize_cancel
    except Exception as e:
        return False
    else:
        return check
    return check

def update_start_permission(access_identity, allowance_val):
    
    try:
        access_object = CrawlerAccess.objects.get(Access_identity__exact=access_identity)
        access_object.authorize_access = allowance_val
        access_object.save()
    except Exception as e:
        return False
    else:
        return True
    return True

def update_cancel_permission(access_identity,allowance_val):
    try:
        access_object = CrawlerAccess.objects.get(Access_identity__exact=access_identity)
        access_object.authorize_cancel = allowance_val
        access_object.save()
    except Exception as e:
        return False
    else:
        return True
    return True


def check_breaker_state(access_identity):
    check = True
    try:
        access_object = Crawler_Breaker.objects.get(identifier__exact=access_identity)
        check = access_object.breaker
    except Exception as e:
        return True
    else:
        return check
    return check

def update_breaker_state(access_identity,allowance_val):
    try:
        access_object = Crawler_Breaker.objects.get(identifier__exact=access_identity)
        access_object.breaker = allowance_val
        access_object.save()
    except Exception as e:
        return False
    else:
        return True
    return True