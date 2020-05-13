import mimetypes
import os
import time
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from django.http import HttpResponse
import base64 , re
from PIL import Image
from io import BytesIO
from accounts.models import SubscribeRequest as RequestModel, User
from search.models import ApiSearchLog
from pathlib import Path



p = Path(__file__).parents[1]

def output(request):

    #getting path
    img_save = os.path.join(p, 'static/img/report/')
    print("path is")
    print(img_save)
    linel = os.path.join(p, 'static/img/report/', 'line.png')
    circlel = os.path.join(p, 'static/img/report/', 'circle.png')
    polarl = os.path.join(p, 'static/img/report/', 'polar.png')
    hitograml = os.path.join(p, 'static/img/report/', 'histogram.png')
    circle2l = os.path.join(p, 'static/img/report/', 'circle2.png')
    report = os.path.join(p, 'adminpanel/templates/adminpanel')
    stylesheet = os.path.join(p, 'userdashboard/templates/userdashboard/', 'report.css')
    reports = os.path.join(p, '', 'report.pdf')

    line = request.POST.get('line')
    circle = request.POST.get('circle')
    histogram = request.POST.get('histogram')
    polar = request.POST.get('polar')
    circle2 = request.POST.get('circle2')
    global img
    def getI420FromBase64(codec):
        base64_data = re.sub('^data:image/.+;base64,', '', codec)
        byte_data = base64.b64decode(base64_data + "==")
        image_data = BytesIO(byte_data)
        global img
        img = Image.open(image_data)


        print("converted")

    if(line):
        print("line detected")
        getI420FromBase64(line)
        img.save(img_save + "line" + '.png', "PNG")
    if(circle):
        getI420FromBase64(circle)
        img.save(img_save  + "circle" + '.png', "PNG")
    if (histogram):
        getI420FromBase64(histogram)
        img.save(img_save  + "histogram" + '.png', "PNG")
    if (polar):
        getI420FromBase64(polar)
        img.save(img_save + "polar" + '.png', "PNG")
    if (circle2):
        getI420FromBase64(circle2)
        img.save(img_save + "circle2" + '.png', "PNG")











    print("report")
    global today_search_logs
    today_subscription_requests = RequestModel.objects.all()[:5]
    today_search_logs = ApiSearchLog.objects.all()[:8]
    print("report = ", report)
    env = Environment(loader=FileSystemLoader(searchpath=report))

    template = env.get_template("report.html")
    template_vars = {"title": "Sales Funnel Report - National",
                     "logs": today_search_logs,
                     "address": "Rawalpindi",
                     "address2": "Islamabad",
                     "content": "images",
                     "line": linel,
                     "circle": circlel,
                     "polar": polarl,
                     "histogram": hitograml,
                     "circle2": circle2l,
                     "ct": "Admin Graph",
                     "ct2": "Logs"}
    html_out = template.render(template_vars)
    print("reports = ", reports)
    print(__file__)
    HTML(string=html_out, base_url=__file__).write_pdf(reports, stylesheets=[stylesheet])
    time.sleep(3)
    fl_path = reports

    filename = 'report(Admin).pdf'

    fl = open(fl_path, 'rb')

    mime_type, _ = mimetypes.guess_type(fl_path)
    response = HttpResponse(fl, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response


