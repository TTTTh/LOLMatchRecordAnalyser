# -*- coding: utf-8 -*-
# Spider.py
# 爬虫，实际工作者

import CONF
import json
import SearchPlayerID
from BloomFilter import BloomFilter

PlayerInfo = ""
CompletedList = ""
Filter = ""

def OpenFile(local):
    try:
        fp = open(local, 'r')
    except Exception, e:
        fp = open(local, 'w')
        fp.close()
        fp = open(local, 'r')
    return fp

def Init():
    global PlayerInfo
    global CompletedList
    global Filter
    print 'Initialization begin.'
    PlayerInfo = OpenFile(CONF.PLAYER_INFO)
    CompletedList = OpenFile(CONF.COMPLETED_LIST)
    #Filter = BloomFilter(0.0001, 10000000)
    Filter = BloomFilter(0.001, 100000)
    print 'Initialization compeleted!'

def RunningSpider(playerName = ''):
    Init()
    if playerName == '':
        playerName = CONF.FIRST_PLAYER
    playerMatchRecordsUrl = SearchPlayerID.SearchPlayerId(playerName)
    #print 'Player', playerName, 'has been found!'
    #print 'search ', playerMatchRecordsUrl





if __name__ == '__main__':
    print 'crawler runner beggin'
    RunningSpider()
