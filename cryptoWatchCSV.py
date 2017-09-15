import requests
import pprint
import json
import time
import datetime
import pprint
import sys
import urllib
import urllib2
import json
import time
import datetime
import hmac, hashlib
import datetime
import time
import re
import os.path
import pymongo


client = pymongo.MongoClient("192.168.169.52", 27017)
db = client.MarketWatchHighRes
f = open('OfficialRates2.csv', 'a', 0)

global firstTime
firstTime = 0

def pushToDB(r):
    q = r.json()["result"]
    post = {"date":time.time()}
    for i in q:
        post[i] = r.json()["result"][i]
    db['cryptowatchdata'].insert(post)

def pricesToCSV():
    global firstTime


    #print r.text
    txtBody = str(r.text)
    #print txtBody
    txtArray = txtBody.split("\n")
    #print txtArray

    finalList = []
    counter = 0
    
    for i in range(0, len(txtArray)):
        #BTCUSD ROWS
        if ('''btcusd"''') in txtArray[i]:
            print txtArray[i]
            finalList.append(txtArray[i])

    for i in range(0, len(txtArray)):   
        #ETHUSD ROWS
        if ('''ethusd"''') in txtArray[i]:
            print txtArray[i]
            finalList.append(txtArray[i])
    
    for i in range(0, len(txtArray)):
        #ALL OTHER BTC ROWS
        if '''btc''' in txtArray[i] and '''btcusd''' not in txtArray[i]:
            print txtArray[i]
            finalList.append(txtArray[i])
    
    for i in range(0, len(finalList)):
        finalList[i] = finalList[i].strip().replace(",", "").replace('''"''', "")

    #printing Header
    if ( firstTime == 0):
        header = 'Date, '
        for entry in finalList:
            header = header + str(re.sub("[^a-zA-Z|:]", "", entry)) + ','
        print header
        f.write(header + "\n")
        firstTime = 1


    line = str(datetime.datetime.now().strftime("%m-%d %H:%M")) + ","
    for entry in finalList:
        line = line + str(re.sub("[^0-9|.]", "", entry)) + ','
    print line
    f.write(line + "\n")
    
    #jay = json.load(r)
    #print jay
    #db.cryptowatch.insert(jay)


def main():
    while 1:
        try:
            pushToDB(requests.get("https://api.cryptowat.ch/markets/prices"))
            time.sleep(10)
            print "data pushed"
        except:
            print "error pushing db/pulling api"
            pass
        
if __name__ == '__main__':
  main()    
