# -*- coding: utf-8 -*-
# Spider.py
# 爬虫，实际工作者

import CONF
import json
import SearchPlayerID
#import Storage
import PlayerMatchAnalyser

from BloomFilter import BloomFilter
from Queue import Queue

PlayerInfoFp = ""
CompletedList = ""
#PlayerNameFilter = ""
#succesPlayerRecords = []
#PlayerNameQueue = ""

def OpenFile(local, tpye = 'r'):
    try:
        fp = open(local, 'r')
    except Exception, e:
        fp = open(local, 'w')
        fp.close()
        fp = open(local, tpye)
    return fp


def Init():
    global PlayerInfoFp
    global CompletedList
    global Filter
    #global PlayerNameQueue

    print 'Initialization begin.'

    #PlayerNameQueue = Queue()
    PlayerInfoFp = open(CONF.PLAYER_INFO, 'a')
    #PlayerInfo = OpenFile(CONF.PLAYER_INFO)
    #CompletedList = OpenFile(CONF.COMPLETED_LIST)
    #Filter = BloomFilter(0.0001, 10000000)
    playerNameQueue = Queue()
    playerNameFilter = BloomFilter(0.001, 100000)
    print 'Initialization compeleted!'

    return playerNameQueue, playerNameFilter


def StorePlayerRecord(PlayerInfDict):
    global PlayerInfo
    #拆解出个人信息
    oneRecord = {}
    oneRecord['PlayerName'] = PlayerInfDict['PlayerName']
    oneRecord['PersonalRating'] = PlayerInfDict['PersonalRating']
    oneRecord['ServerName'] = PlayerInfDict['ServerName']
    oneRecord['LocalInfPath'] = CONF.JSON_PATH + PlayerInfDict['PlayerName'] + '.json'

    #保存对局信息
    fp = open(oneRecord['LocalInfPath'], 'wb')
    line = json.dumps(PlayerInfDict)
    fp.write(line)
    fp.close()

    #将已经完成的玩家信息保存到文件里
    #succesPlayerRecords.append(oneRecord)
    line = json.dumps(oneRecord)
    #print 'in storage, line =', line
    PlayerInfoFp.write(line)



#提取某一个对局中的玩家的名字
def ExtractPlayerNameInSigleMatch(teamRecordDict):
    playerNames = []
    for playerRecord in teamRecordDict['PlayerRecords']:
        playerNames.append(playerRecord['playerID'])
    return playerNames

#提取某一个玩家的记录中出现的新名字
def ExtractFurtherPlayerName(playerInfDict, playerNameFilter):
    recordList = playerInfDict['MatchRecord']
    furtherPlayerName = []
    for record in recordList:
        #print 'analyse record'
        tmpList = ExtractPlayerNameInSigleMatch(record)
        for name in tmpList:
            if playerNameFilter.exsist(name) == False:
                playerNameFilter.insert(name)
                furtherPlayerName.append(name)

    return furtherPlayerName



def RunningSpider(playerName = ''):
    playerNameQueue, playerNameFilter = Init()

    if playerName == '':
        playerName = CONF.FIRST_PLAYER
    playerNameQueue.put(playerName)
    playerNameFilter.insert(playerName)
    #广度优先开始抓取
    while playerNameQueue.empty() == False:
        curPlayerName = playerNameQueue.get()
        #搜索这个用户对应的网页
        playerMatchRecordsUrl = SearchPlayerID.SearchPlayerId(curPlayerName)
        #提取用户的战绩等等信息
        playerInfDict = PlayerMatchAnalyser.AnalysisRecord(playerMatchRecordsUrl, curPlayerName)
        if playerInfDict != None :
            StorePlayerRecord(playerInfDict)
            #print 'player', playerName, '\'s record analyse completed'
            furtherPlayerName = ExtractFurtherPlayerName(playerInfDict)
            for name in furtherPlayerName:
                print 'name =', name
        else:
            print 'player', playerName, '\'s record analyse error'

def Close():
    #将一些信息保存到文件当中
    #读取原信息并追加新的信息
    playerInfoFp = OpenFile(CONF.PLAYER_INFO)
    playerInfoFp.close()
    originalList = json.loads(playerInfoFp.read())
    originalList.extend(succesPlayerRecords)

    #把新的信息写入文件
    playerInfoFp = open(CONF.PLAYER_INFO, 'wb')
    playerInfoFp.write(json.dumps(originalList))
    playerInfDict.close()

    #输出结束信息
    print 'crawler ', len(playerInfoFp), 'player Info'





if __name__ == '__main__':
    print 'crawler runner beggin'
    RunningSpider()
