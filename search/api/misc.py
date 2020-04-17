import os
import re


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
