# -*- coding: utf-8 -*-
# Recovery.py

import json
import lxml
import CONF

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

def RecoveryDownloadRecord(PlayerNameQueue, PlayerNameFilter):
    playerInfoFp = open(CONF.PLAYER_INFO, 'r')
    lines = playerInfoFp.readlines()
    for line in lines:
        #这是一个成功的信息，把这个玩家的ID插进去
        lineDict = json.loads(line)
        PlayerNameFilter.insert(lineDict['PlayerName'])

    #分析失败玩家的文件的记录
    failedIDList = open(CONF.FAILED_ID_LIST, 'r')
    failedLines = failedIDList.readlines()
    for name in failedLines:
        PlayerNameFilter.insert(name)

    #分析每个成功玩家的记录，将记录中未被抓取的名字填入队列
    for line in lines:
        lineDict = json.loads(line)
        #print lineDict['PlayerName'].encode('utf-8')

        playerInfoFp = open(lineDict['LocalInfPath'], 'r')
        playerInfDict = json.loads(playerInfoFp.read())
        newPlayerNameList = ExtractFurtherPlayerName(playerInfDict, PlayerNameFilter)
        for name in newPlayerNameList:
            print 'found needed analyse player', name.encode('utf-8')
            PlayerNameQueue.put(name)

    playerInfoFp.close()


if __name__ == '__main__':
    import Queue
    import BloomFilter

    que = Queue.Queue()
    fil = BloomFilter.BloomFilter(0.1,1000)
    RecoveryDownloadRecord(que, fil)
