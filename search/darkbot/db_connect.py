import pymongo
from search.darkbot.tor_connection import disconnect
def insertInChannelCollection():
    mycol = mydb["channel"]
    mylist = [
        {"channel_name": "CAVETOR", "channel_url": "http://cavetord6bosm3sl.onion/blogs/buy-high-quality-real-registered-passpor/buy-high-quality-real-registered-passpor.html"},
        {"channel_name": "MAIL THREAD", "channel_url": "http://vtg3zdwwe4klpx4t.onion/static/robertotto25@gmail.com/msg10138.html"},
        {"channel_name": "FORUM CLONE CARD", "channel_url": "http://cardingeokeo3r6z.onion/wisdom/threaddc04dc04dc04.html?file=selling-paypal-accounts-with-balance-upto-5000dollars"},
    ]
    mycol.insert_many(mylist)

def getChannels():
    #print('run ')
    disconnect()
    while True:
        try:
            client = pymongo.MongoClient("mongodb+srv://daud123:daud123@cluster0-4551z.mongodb.net/test?retryWrites=true")
            mydb = client['darkbot']
            mycol = mydb['channel']
            url=[]
            mydoc = mycol.find()
            for each in mydoc:
                # print(each["channel_url"])
                url.append([each["channel_url"],each["channel_name"]])
            client.close()
        except (pymongo.errors.ConfigurationError,pymongo.errors.ConnectionFailure) as e:
            print(e)
            continue
        else:
            print("Connected to mongoDB")
            break
    return url

# if __name__ == "__main__":
#     l = getChannels()
    '''for each in l:
        print(each)'''

