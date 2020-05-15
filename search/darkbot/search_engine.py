from search.darkbot.tor_connection import connect_tor # for running as django
# from tor_connection import connect_tor # for running as a script
import requests
from bs4 import BeautifulSoup
import concurrent.futures

def search_engine(input):
    l = []
    headers = {
        'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) "
                      "AppleWebKit/535.11 (KHTML, like Gecko) "
                      "Ubuntu/10.10 Chromium/17.0.963.65 "
                      "Chrome/17.0.963.65 Safari/535.11"}
    search_engines=["http://msydqstlz2kzerdg.onion","http://grams7enufi7jmdl.onion/","http://gjobqjj7wyczbqie.onion","http://hss3uro2hsxfogfq.onion","http://xmh57jrzrnw6insl.onion"]
    payload = {'q': input}
    proxy = connect_tor()
    obj = {}
    obj['headers'] = headers
    obj['payload'] = payload
    obj['proxy'] = proxy
    with concurrent.futures.ThreadPoolExecutor() as executor:
        t1 = executor.submit(searchengine2, obj)
        t2 = executor.submit(searchengine1, obj)
        l.extend(t1.result())
        l.extend(t2.result())
    return l

def searchengine1(obj):
    l1 = []
    try:
        response = requests.get('http://xmh57jrzrnw6insl.onion/4a1f6b371c/search.cgi', headers=obj["headers"], params= obj["payload"], proxies=obj["proxy"], timeout=(10, 10))
    except Exception as e:
        print("exception in searchengine1")
        return []
    else:
        html = BeautifulSoup(response.text, 'html.parser')
        for each_dt in html.find_all("dt"):
            each_a = each_dt.findChildren("a", recursive=False)
            for a in each_a:
                l1.append([a.get_text().strip(' '), a["href"]])
        j = 0
        for each_dd in html.find_all("dd"):
            each_small = each_dd.find("small")
            aaa = each_small.get_text().strip("[Cached copy")
            if aaa and aaa != "]":
                l1[j].append(aaa)
                j = j + 1
    return l1

def searchengine2(obj):
    l1 = []
    try:
        response = requests.get('http://gjobqjj7wyczbqie.onion', headers=obj["headers"], params=obj["payload"], proxies= obj["proxy"], timeout=(10, 10))
    except Exception as e:
        print("exception in searchengine2")
        return []
    else:
        print('hello')
        html = BeautifulSoup(response.text, 'html.parser')
        for each_h2 in html.find_all("h2"):
            l1.append([each_h2.get_text(), each_h2.a["href"]])
        i = 0
        for each_h3 in html.find_all('h3'):
            text = str(each_h3.nextSibling).strip()
            text = text.strip("</br>")
            text = str(text)
            if text:
                l1[i].append(text)
                i = i + 1
    return l1




# if __name__ == "__main__":
#     print('started')
#     mylist = search_engine("food")
#     for e in mylist:
#         print('new')
#         print(e)