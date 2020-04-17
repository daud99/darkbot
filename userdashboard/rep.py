import mimetypes
import os
import time
from pathlib import Path
from wsgiref.util import FileWrapper

from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from django.http import HttpResponse
import base64 , re
from PIL import Image
from io import BytesIO



from accounts.models import SubscribeRequest as RequestModel, User
from search.models import SearchLog

p = Path(__file__).parents[1]
def output(request):

    img_save=os.path.join(p, 'static/img/report/')
    circleql= os.path.join(p, 'static/img/report/', 'circleq.png')
    histogramtl=os.path.join(p, 'static/img/report/', 'histogramt.png')
    circlesl=os.path.join(p, 'static/img/report/', 'circles.png')
    reportu =os.path.join(p, 'userdashboard/templates/userdashboard')
    stylesheet = os.path.join(p, 'userdashboard/templates/userdashboard/', 'report.css')
    reports = os.path.join(p, '', 'reportu.pdf')


    #Getting base64 links of canvas
    circleq = request.POST.get('circleq')
    histogramt = request.POST.get('histogramt')
    circles = request.POST.get('circles')


    #converting base64
    global img
    def getI420FromBase64(codec):
        base64_data = re.sub('^data:image/.+;base64,', '', codec)
        byte_data = base64.b64decode(base64_data + "==")
        image_data = BytesIO(byte_data)
        global img
        img = Image.open(image_data)


    #saving
    if(circleq):
        getI420FromBase64(circleq)
        img.save(img_save + "circleq" + '.png', "PNG")
    if (histogramt):
        getI420FromBase64(histogramt)
        img.save(img_save  + "histogramt" + '.png', "PNG")
    if (circles):
        getI420FromBase64(circles)
        img.save(img_save + "circles" + '.png', "PNG")


    #Getting UserLogs
    currentuser = User.objects.get(pk=request.user.id)
    today_search_logs = SearchLog.objects.filter(user=currentuser).order_by('-search_time')[:8]

    #Getting html template
    env = Environment(loader=FileSystemLoader(searchpath=reportu))
    template = env.get_template("report.html")

    #writing to template
    template_vars = {"title": "Final Report(Users)",
                     "logs": today_search_logs,
                     "circleq": circleql,
                     "histogramt": histogramtl,
                     "circles": circlesl,
                     "ct": "Users Graph",
                     "ct2": "Logs"}
    html_out = template.render(template_vars)
    HTML(string=html_out, base_url=__file__).write_pdf(reports,
                                                       stylesheets=[
                                                           stylesheet])

    #Downloading Pdf
    time.sleep(3)
    fl_path = reports
    filename = 'report(User).pdf'
    fl = open(fl_path, 'rb')
    mime_type, _ = mimetypes.guess_type(fl_path)
    response = HttpResponse(fl, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response











