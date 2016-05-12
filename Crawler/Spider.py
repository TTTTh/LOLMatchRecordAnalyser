# -*- coding: utf-8 -*-
# Spider.py
# 爬虫，实际工作者

import CONF
import json
import SearchPlayerID
#import Storage
import Recovery
import PlayerMatchAnalyser

from BloomFilter import BloomFilter
from Queue import Queue

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

PlayerInfoFp = ""
CompletedList = ""
#PlayerNameFilter = ""
#succesPlayerRecords = []
#PlayerNameQueue = ""
RecordCnt = 0

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
    playerNameQueue = Queue()
    playerNameFilter = BloomFilter(0.001, 1000000)
    Recovery.RecoveryDownloadRecord(playerNameQueue, playerNameFilter)

    print 'Initialization compeleted!'

    return playerNameQueue, playerNameFilter


def StorePlayerRecord(PlayerInfDict):
    global PlayerInfoFp
    global RecordCnt
    #拆解出个人信息
    oneRecord = {}
    oneRecord['PlayerName'] = PlayerInfDict['PlayerName'].encode('utf-8')
    oneRecord['PersonalRating'] = PlayerInfDict['PersonalRating'].encode('utf-8')
    oneRecord['ServerName'] = PlayerInfDict['ServerName'].encode('utf-8')
    oneRecord['LocalInfPath'] = CONF.JSON_PATH + PlayerInfDict['PlayerName'] + '.json'

    #保存对局信息
    fp = open(oneRecord['LocalInfPath'], 'wb')
    line = json.dumps(PlayerInfDict)
    fp.write(line)
    fp.close()

    #将已经完成的玩家信息保存到文件里
    #succesPlayerRecords.append(oneRecord)
    line = json.dumps(oneRecord) + '\n'
    print 'in storage, line =', line
    PlayerInfoFp.write(line)
    RecordCnt = RecordCnt + 1
    if RecordCnt == 10:
        print 'save one'
        PlayerInfoFp.close()
        PlayerInfoFp = open(CONF.PLAYER_INFO, 'a')
        RecordCnt = 0


#提取某一个对局中蓝队或者紫队的玩家的名字
def ExtractPlayerNameInSigleMatch(teamRecordDict):
    playerNames = []
    for playerRecord in teamRecordDict['PlayerRecords']:
        playerNames.append(playerRecord['PlayerId'])
    return playerNames

#提取某一个玩家的记录中出现的新名字
def ExtractFurtherPlayerName(playerInfDict, playerNameFilter):
    recordList = playerInfDict['MatchRecord']
    furtherPlayerName = []
    for record in recordList:
        #print 'analyse record'
        tmpList = ExtractPlayerNameInSigleMatch( record[ 'BlueRecordsDict' ] )
        tmpList.extend( ExtractPlayerNameInSigleMatch( record['PurpleRecordsDict' ] ) )
        for name in tmpList:
            #print 'name =', name.encode('utf-8')
            if playerNameFilter.exist(name) == False :
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
        print 'Player', curPlayerName.encode('utf-8'), '\' s record is being analysed!'
        #搜索这个用户对应的网页
        playerMatchRecordsUrl = SearchPlayerID.SearchPlayerId(curPlayerName)
        if playerMatchRecordsUrl == None:
            continue
        #提取用户的战绩等等信息
        playerInfDict = PlayerMatchAnalyser.AnalysisRecord(playerMatchRecordsUrl, curPlayerName)
        if playerInfDict != None :
            StorePlayerRecord(playerInfDict)
            #print 'player', playerName, '\'s record analyse completed'
            furtherPlayerName = ExtractFurtherPlayerName(playerInfDict,playerNameFilter)
            for name in furtherPlayerName:
                #print 'name =', name
                print 'Player', name.encode('utf-8'), 'has been found, and joined the queue'
                playerNameQueue.put(name)
        else:
            print 'player', curPlayerName, '\'s record analyse error'

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
