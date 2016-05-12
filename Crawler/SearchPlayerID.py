# -*- coding: utf-8 -*-
# SearchPlayerId.py

import urllib
import CONF
from lxml import etree

AllowServerList = CONF.ALLOWE_SERVER

def to_bytestring(s, enc='utf-8'):
    if s:
        if isinstance(s, str):
            return s
        else :
            return s.encode(enc)

def AddErrorPalyerName(playerName, e):
    print 'player', to_bytestring(playerName), 'searching error!'
    print e
    try:
        fp = open(CONF.FAILED_ID_LIST, 'a')
    except Exception, e:
        fp = open(CONF.FAILED_ID_LIST, 'w')
        fp.close()
        fp = open(CONF.FAILED_ID_LIST, 'a')

    fp.write(playerName + '\n')
    fp.close()

# //*[@id="searchUL"]/li
#//*[@id="searchUL"]/li/a/p
def SearchPlayerId(playerName):
    global AllowServerList

    url = CONF.SEARCH_URL_PREFIX + to_bytestring(playerName)
    #print 'Search Player', playerName
    #print 'url =', url
    tmpLocal = 'tmpIdPage.html'
    urllib.urlretrieve(url, tmpLocal)
    fp = open(tmpLocal, 'r')
    #fp = urllib.urlopen(url)
    tree = etree.HTML(fp.read())
    xpathStr = '//*[@id="searchUL"]/li/a/@href'

    try:
        playerLink = tree.xpath(xpathStr)[0]
    except Exception, e:
        AddErrorPalyerName(playerName, e)
        return None

    #print 'playerLink =', playerLink
    ServerName = tree.xpath('//*[@id="searchUL"]/li/a/p')[0].text.split(' ')[0]
    ServerName1 = ServerName.encode('utf-8')

    for allowServer in AllowServerList:
        if ServerName1 == allowServer:
            return playerLink
        else:
            return
