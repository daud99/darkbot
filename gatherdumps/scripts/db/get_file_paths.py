from gatherdumps.models import FilePath
def get_email_file_path(identity):
    
    try:
            checkpoint = FilePath.objects.get(identifier__exact=identity)
       
    except Exception as e:
        return None
    else:

        return [checkpoint.source, checkpoint.path, checkpoint.break_point]


def update_file_path(identity, status):
    try:
        FilePath.objects.filter(identifier__exact=identity).update(status=status)

    except Exception as e:
        return None

