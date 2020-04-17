from gatherdumps.models import Country, CardDump, CardCvv, Email_passwords, CardMarket, Checkpoint

def get_checkpoint(identity):
    countries= Country.objects.all()
    while(True):
        try:
            checkpoint = Checkpoint.objects.get(Checkpoint_identity__exact=identity)
            
            
        except Exception as e:
            return None
        else:
            if (checkpoint.next_index<0 or checkpoint.next_index >= countries.count()):
                update_checkpoint(checkpoint, 0)
                continue
            else:

                return checkpoint
        

def get_index_checkpoint(identity):
        try:
            checkpoint = Checkpoint.objects.get(Checkpoint_identity__exact=identity)
       
        except Exception as e:
            return None
        else:
            return checkpoint

    
def update_checkpoint(checkpoint, index):
    checkpoint.next_index = index
    checkpoint.save()
    print('Updated checkpoint')




    