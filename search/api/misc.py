import os
import re
from gatherdumps.models import Email_passwords

def getPath(basepath, lastpath):
    return os.path.join(basepath, lastpath)

def returnDomain(email):
  return email.rsplit("@")[1].lower()

def splitEmail(email):
  email = email.rsplit("@")
  s = [email[0].lower()]
  s.extend(email[1].rsplit("."))
  if len(s) == 3:
    s.append("")
  return s

def returnTwo(email):
  two = email.rsplit("@")
  return [two[0].lower(), two[1].lower()]


def isDigitOrNumber(c):
  return ((c >= 'a' and c <= 'z') or (c >= '0' and c <= '9'))


def finalizeRegex(input_regex, type):
  input_regex = re.escape(input_regex)
  if input_regex[0] != r'\\' and input_regex[1] != r'*':
    print('yes here where it should not be')
    input_regex = r'^' + input_regex
  if len(input_regex) > 1:
    if input_regex[-2] != r'\\' and input_regex[-1] != r'*':
      input_regex = input_regex + r'$'
  if type in ["email","domain","username","phonenumber","ipaddress"]:
    input_regex = input_regex.replace('\*', r'[a-zA-Z0-9\-_.]*')
  else:
    input_regex = input_regex.replace('\*', r'.*')
  return input_regex

def formatDate(date):
  return date.strftime("%Y-%m-%d %H:%M:%S")


def checkRecordUniqueness(func):
  def wrapper(*args):
    if "email" in args[0]:
      email = args[0]["email"]
    else:
      email = None
    if "password" in args[0]:
      password = args[0]["password"]
    else:
      password = None
    if "source" in args[0]:
      source = args[0]["source"]
    else:
      source = "unknown"
    if "username" in args[0]:
      username = args[0]["username"]
    else:
      username = None

    if email != None and email != '' and username in ["", None]:
      record = Email_passwords.objects.filter(email=email, password=password, source=source).count()
    elif username != None and username != '' and email in ["", None]:
      record = Email_passwords.objects.filter(username=username, password=password, source=source).count()
    else:
      record = Email_passwords.objects.filter(**args[0]).count()

    if record != 0:
      print("Record already exist Duplication find")
      return
    else:
      print("storing in DB as it is not found in DB")
      return func(args[0])

  return wrapper
