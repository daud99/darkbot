
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'q*%r*kevzyp_s)36=ec2)kljdfklsajdflkj34%&v+745z1i+j5z!1h@s#)^!nm'

# SECURITY WARNING: don't run with debug turned on in production!
#DEBUG = True
DEBUG = False

ALLOWED_HOSTS = ["85.195.114.172"]
#ALLOWED_HOSTS = ["*"]

# setting for leak check api
LEAK_CHECK_KEY = '2a158c46accb55127856b57ea2b854dc342a0e04'
LEAK_CHECK_URL = 'https://leakcheck.net/api/'


# setting for we leak info api

WE_LEAK_KEY = '7635bf59b71570492ace2fb104259dff99d6bed6'
WE_LEAK_URL = 'https://api.weleakinfo.com/v3/search'
