from django.shortcuts import render
from .forms import SubscribeRequestForm,UserCreateForm
from .models import SubscribeRequest
from django.views.generic import CreateView,TemplateView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect,HttpResponse
from django.core.mail import send_mail
from django.contrib.messages.views import SuccessMessageMixin
from accounts.script import sendmail,iplisting


template_name = 'accounts'
# Create your views here.

# class SignUp(CreateView):
#     form_class = UserCreateForm
#     success_url = reverse_lazy('dashboard:start')
#     template_name = 'accounts/signup.html'
#
#     def form_valid(self, form):
#         yahopass = form.cleaned_data['password2']
#         # print('password before form .save function called',form.cleaned_data['password2'])
#         self.object = form.save()
#         # do something with self.object
#         # remember the import: from django.http import HttpResponseRedirect
#         print('lets see it do print the email or not')
#         iplisting.addip(self.object.ip_address)
#         subject = 'Darkbot Credentials'
#         from_email = sendmail.EMAIL_HOST_USER
#         message = 'Congratulation! Your request for Darkbot is successfully accepted your email: {} and password is {}.'.format({yahopass},{self.object.email});
#         to_list = [self.object.email,'daudahmed@zoho.com']
#         send_mail(subject,message,from_email,to_list)
#         print('CHECK YOUR GMAIL')
#         print(self.object.email)
#         print(self.object.password)
#         return HttpResponseRedirect(self.get_success_url())

class SubscribeMakeRequest(SuccessMessageMixin,CreateView):
    redirect_field_name = '/'
    form_class = SubscribeRequestForm
    model = SubscribeRequest
    success_message = 'Your subscription request is successfully sended to admin'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['ip_address'] = get_client_ip(self.request)
        return context

def get_client_ip(request):
    
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    '''
    ip = request.COOKIES['ip']
    '''
    print('current ip address is : ', ip)
    if (request.COOKIES.get('ip')):
        ip = request.COOKIES.get('ip')
    return ip




