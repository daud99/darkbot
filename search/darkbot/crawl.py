#print('in crawl --name__ is'+__name__)
import socket
import socks
# from search.darkbot.db_connect import getChannels
# from search.darkbot.link import LinkNode


from search.darkbot.tor_connection import connect_tor, disconnect
from search.darkbot.crawler_2 import Crawler
from search.models import Channels, IndexEmail
from gatherdumps.models import CrawlerAccess, Checkpoint
from gatherdumps.scripts.common.check_crawler_access import check_cancel_permission, check_start_permission
l = []
db_con = 0
'''def connect_db():
    print("Connecting to DB")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.socket = socks.socksocket


def connect_tor():
    """ Establishes connection to port

    Assumes port is bound to localhost, if host that port is bound to changes
    then change the port

    Args:
        address: address for port to bound to
        port: Establishes connect to this port
    """
    address = "127.0.0.1"
    port = 9050
    print("Connecting to tor")
    socks.set_default_proxy(socks.PROXY_TYPE_SOCKS5, address, port)
    socket.socket = socks.socksocket  # Monkey Patch our socket to tor socket

    def getaddrinfo(*args):
        """
        Overloads socket function for std socket library
        Check socket.getaddrinfo() documentation to understand parameters.
        Simple description below:
        argument - explanation (actual value)
        socket.AF_INET - the type of address the socket can speak to (IPV4)
        sock.SOCK_STREAM - creates a stream connecton rather than packets
        6 - protocol being used is TCP
        Last two arguments should be a tuple containing the address and port
        """
        print("getaddrinfo function do execute actually")
        return [(socket.AF_INET, socket.SOCK_STREAM, 6,
                 '', (args[0], args[1]))]
    socket.getaddrinfo = getaddrinfo'''

def get_channels():
    url = []
    all_channels = Channels.objects.all()
    checkpoint = Checkpoint.objects.get(Checkpoint_identity__exact=1001)
    
    start_index = checkpoint.next_index
    if (start_index >=len(all_channels)):
        start_index = 0
    for i in range(start_index, len(all_channels)):
        url.append([all_channels[i].channel_url, all_channels[i].channel_name])
    #print(url)
    return url

def emails_with_channel():
    if (check_start_permission(200) == False):
        return False
    final_list=[]
    l = get_channels()
    #connect_tor()

    for i, x in enumerate(l):
        
        try:
            node = Crawler(x[0],x[1])
            # in below line we are calling emails property on object node
            #print('for : ', i)
            foundemail = node.BFS()
            #node.children
            #links_list = node.links
            #l.extend(lisks_list) # adding crawled links
            #print(links_list)
            #for each_email in foundemail:
                #print(each_email)

            #final_list.extend(foundemail)
            if (foundemail):
                checkpoint = Checkpoint.objects.get(Checkpoint_identity__exact=1001)
                test = checkpoint.next_index + 1
                if (test >= len(l)):
                    test = 0
                checkpoint.next_index = test
                checkpoint.save()
        except (ValueError, HTTPError, ConnectionError) as err:
            #print(err)
            raise err
        print('finalllllll')
        # for mail in final_list:
        #     current_email = IndexEmail()
        #     current_email.channel_name = mail[2]
        #     current_email.channel_url = mail[1]
        #     current_email.email = mail[0]
        #     current_email.save()
        final_list.clear()
        
    return True
        # print(x["channel_url"])

# if __name__ == '__main__':
#     emails_with_channel()