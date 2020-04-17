import csv
from gatherdumps.models import CardCvv, CardDump

def read_cvvs(path, typi):
    with open(path) as f:
        rows = csv.reader(f)
        for row in rows:
            if typi == 'cvv':
                storeInDBCVV(*row)
            elif typi == 'dump':
                storeInDBDUMP(*row)



def storeInDBCVV(bin_no,card_type,card_category,refund,card_mark,expiry,name,city,state,zip_no,bank,country,base):
    cvv = CardCvv(bin_no=bin_no, card_type=card_type, card_category=card_category, refund=refund, card_mark=card_mark,expiry=expiry,name=name,city=city,state=state,zip_no=zip_no,bank=bank,country=country,base=base, price="30$", source="http://brocardy4tvfelfo.onion/")
    cvv.save()

def storeInDBDUMP(bin_no,track,carr,card_type,card_category,refund,card_mark,bank,country,dumped_in,base):
    dump = CardDump(bin_no=bin_no, track=track,carr=carr,card_type=card_type,card_category=card_category,refund=refund,card_mark=card_mark,bank=bank,country=country,dumped_in=dumped_in,base=base,price="30$",source="http://brocardy4tvfelfo.onion/")
    dump.save()


