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
db = client.cryptowatch
f = open('OfficialRates2.csv', 'a', 0)

global firstTime
firstTime = 0


def pricesToCSV():
    global firstTime

    r = requests.get("https://api.cryptowat.ch/markets/prices")
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
    try:
        while 1:
            pricesToCSV()
            time.sleep(10)
    except KeyboardInterrupt:
        io_loop.stop()
        f.close()
        sys.exit()
    
        
if __name__ == '__main__':
  main()    
