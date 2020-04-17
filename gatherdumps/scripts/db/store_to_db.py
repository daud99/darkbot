from django.db import models
from gatherdumps.models import CardDump as CD, CardCvv as CC

def store_dumps(dumps_list):
    for x in dumps_list:
        try:

                p = CD.objects.create(bin_no=x['bin_no'],track=x['track'],carr=x['carr'],
                                card_type=x['card_type'],
                                card_category=x['card_category'],
                                refund=x['refund'],card_mark=x['card_mark'],
                                bank=x['bank'],country=x['country'],
                                dumped_in=x['dumped_in'],base=x['base'],
                                quantity=x['quantity'],price=x['price'],
                                source=x['source'],date=x['date'])
        except Exception as e:
                print(e)
                print('Exception while saving')
                continue

def store_cvvs(cvvs_list):
        for x in cvvs_list:
                try:

                        p = CC.objects.create(bin_no=x['bin_no'],
                                        card_type=x['card_type'],
                                        card_category=x['card_category'],
                                        refund=x['refund'],card_mark=x['card_mark'],
                                        expiry = x['expiry'], name= x['name'],
                                        city =x['city'], state=x['state'],
                                        zip_no = x['zip_no'],
                                        bank=x['bank'],country=x['country'],
                                        base=x['base'],
                                        price=x['price'],
                                        source=x['source'],date=x['date'])
                except Exception as e:
                        print(e)
                        print('Exception while saving')
                        continue
def remove_all():
        CC.objects.all().delete()
        CD.objects.all().delete()

