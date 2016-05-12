# -*- coding: utf-8 -*-
# SearchPlayerId.py

import urllib
import CONF
from lxml import etree

AllowServerList = CONF.ALLOWE_SERVER

# //*[@id="searchUL"]/li
#//*[@id="searchUL"]/li/a/p
def SearchPlayerId(playerName):
    global AllowServerList
    url = CONF.SEARCH_URL_PREFIX + playerName
    print 'Search Player', playerName,
    print 'url =', url
    fp = urllib.urlopen(url)
    tree = etree.HTML(fp.read())
    xpathStr = '//*[@id="searchUL"]/li/a/@href'
    playerLink = tree.xpath(xpathStr)[0]
    #print 'playerLink =', playerLink
    ServerName = tree.xpath('//*[@id="searchUL"]/li/a/p')[0].text.split(' ')[0]
    ServerName1 = ServerName.encode('utf-8')

    for allowServer in AllowServerList:
        if ServerName1 == allowServer:
            return playerLink
        else:
            return
