from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from search.models import Messages
from django.contrib import messages
from PIL import Image
from io import BytesIO
import base64 , re , time
from dark_bot import settings
import datetime

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return redirect('/adminpanel')
    if not request.COOKIES.get('ip'):
        
        print('need to set cookie')
        #set_cookies(request)
        #return redirect('http://127.0.0.1:8000/')
        
    #print(request.headers)
    print('cookie', request.COOKIES.get('ip'))
    return render(request,'index.html')


def contact(request):
    if request.method == 'POST':
        sender_name = request.POST.get('name')
        sender_email = request.POST.get('email')
        sender_message = request.POST.get('message')

        msg = Messages(sender_name=sender_name, sender_email=sender_email, sender_message=sender_message)
        msg.save()
        messages.success(request,'Your message is successfulyy sended')
        return render(request, 'contact.html')
    else:
        return render(request,'contact.html')

def download(request):
    print('request is received')
    if request.method == 'POST':
        line = request.POST.get('line')
        name = request.POST.get('name')
        # print('line')
        # print(line)
        # now = datetime.datetime.now()
        # now = str(now)
        if(line):
            line_img = getI420FromBase64(line)
            line_img.save(getPath() + name , "PNG")
    return HttpResponse('Return data to ajax call')

def getI420FromBase64(codec):
    base64_data = re.sub('^data:image/.+;base64,', '', codec)
    byte_data = base64.b64decode(base64_data + "==")
    image_data = BytesIO(byte_data)
    img = Image.open(image_data)
    return img

def getPath():
    return settings.STATICFILES_DIRS[0] + '/img/report/'
