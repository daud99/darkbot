from search.darkbot.tor_connection import connect_tor,disconnect
#from tor_connection import connect_tor,disconnect
import requests
from bs4 import BeautifulSoup,NavigableString,Tag

def search_engine(input):
    l1 = []
    print("1")
    #connect_tor()
    print("2")
    headers = {
        'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) "
                      "AppleWebKit/535.11 (KHTML, like Gecko) "
                      "Ubuntu/10.10 Chromium/17.0.963.65 "
                      "Chrome/17.0.963.65 Safari/535.11"}
    search_engines=["http://msydqstlz2kzerdg.onion","http://grams7enufi7jmdl.onion/","http://gjobqjj7wyczbqie.onion","http://hss3uro2hsxfogfq.onion","http://xmh57jrzrnw6insl.onion"]
    payload = {'q': input}
    # try:
    proxy = connect_tor()
    try:
        response = requests.get('http://xmh57jrzrnw6insl.onion/4a1f6b371c/search.cgi', headers=headers ,params=payload, proxies= proxy, timeout=(20,70))
    except Exception as e:
        print("Exception at search engine 1")
    else:

        html = BeautifulSoup(response.text, 'html.parser')
        print(html)
        # dt = html.find("dt")
        # children = dt.findChildren("a", recursive=False)
        for each_dt in html.find_all("dt"):
            each_a = each_dt.findChildren("a", recursive=False)
            for a in each_a:
                print(a.get_text().strip(' '))
                print(a["href"])
                l1.append([a.get_text().strip(' '), a["href"]])
        j = 0
        for each_dd in html.find_all("dd"):
            each_small = each_dd.find("small")
            aaa = each_small.get_text().strip("[Cached copy")
            if aaa and aaa != "]":
                l1[j].append(aaa)
                # print("text is: "+aaa)
                # print("j is : ",j)
                j = j + 1
    i = len(l1)
    payload = {'q': input}
    proxy = connect_tor()
    try:
        response = requests.get('http://gjobqjj7wyczbqie.onion', headers=headers, params=payload, proxies=proxy, timeout=(20,70))
    except Exception as e:
        print('Exception at search engine 2')
    else:
        print('hello')
        html = BeautifulSoup(response.text, 'html.parser')
        for each_h2 in html.find_all("h2"):
            l1.append([each_h2.get_text(), each_h2.a["href"]])
        for each_h3 in html.find_all('h3'):
            text = str(each_h3.nextSibling).strip()
            text = text.strip("</br>")
            text = str(text)
            print("i is", i)
            print("yes")
            if text:
                print('here')
                l1[i].append(text)
                i = i + 1
                '''if i < len(l1):
                    l1[i].extend(str(text))
                    #print(l1[i])'''
                # print(text)
    # except Exception as e:
    #     print("internet problem")
    #     print(e)
    # else:
    #     print("Successfully connected to internet")
    #disconnect()
    return l1
#
#
# if __name__ == "__main__":
#     print('started')
#     mylist = search_engine("food")
#     for e in mylist:
#         print('new')
#         print(e)
#         #pass
