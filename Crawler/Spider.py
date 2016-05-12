# -*- coding: utf-8 -*-
# Spider.py
# 爬虫，实际工作者

import CONF
import json
import SearchPlayerID
import Sortage
import PlayerMatchAnalyser

from BloomFilter import BloomFilter

PlayerInfo = ""
CompletedList = ""
Filter = ""
succesPlayerRecords = []
def OpenFile(local):
    try:
        fp = open(local, 'r')
    except Exception, e:
        fp = open(local, 'w')
        fp.close()
        fp = open(local, 'r')
    return fp

def StoragePlayerRecord(PlayerInfDict):
    global succesPlayerRecords
    #拆解出个人信息
    oneRecord = {}
    oneRecord['playerName'] = PlayerInfDict['playerName']
    oneRecord['PersonalRating'] = PlayerInfDict['PersonalRating']
    oneRecord['ServerName'] = PlayerInfDict['ServerName']
    oneRecord['LocalInfPath'] = CONF.JSON_PATH + PlayerInfDict['playerName'] + '.json'

    #保存对局信息
    fp = open(oneRecord['LocalInfPath'], 'wb')
    line = json.dumps(PlayerInfDict)
    fp.write(line)
    fp.close()

    #将已经完成的玩家信息保存到文件里



def Init():
    global PlayerInfo
    global CompletedList
    global Filter
    print 'Initialization begin.'
    PlayerInfo = OpenFile(CONF.PLAYER_INFO)
    #CompletedList = OpenFile(CONF.COMPLETED_LIST)
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
    playerInfDict = PlayerMatchAnalyser.AnalysisRecord(playerMatchRecordsUrl, playerName)
    if playerInfDict != None :
        print 'player', playerName, '\'s record analyse completed'
    else:
        print 'player', playerName, '\'s record analyse error'



if __name__ == '__main__':
    print 'crawler runner beggin'
    RunningSpider()
