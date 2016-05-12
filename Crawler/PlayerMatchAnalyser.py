# -*- coding: utf-8 -*-
# PlayerMatchAnalyser.py

import urllib
import json
import CONF
from lxml import etree


def ExtractPlayerRecord(playerRecord):
    playerRecordDict = {}
    chmpnName = playerRecord.xpath('./td[1]/div/div[1]/img/@title')[0]
    playerRecordDict['chmpnName'] = chmpnName

    skill1 = playerRecord.xpath('./td[1]/div/div[2]/div[1]/img[1]/@src')[0]
    skill2 = playerRecord.xpath('./td[1]/div/div[2]/div[1]/img[2]/@src')[0]
    playerRecordDict['Skills'] = [skill1, skill2]

    playerID = playerRecord.xpath('./td[1]/div/div[2]/h6/a')[0].text
    playerRecordDict['PlayerId'] = playerID

    #计算召唤师KDA
    playerKDA = playerRecord.xpath('./td[2]/p')[0].text
    playerRecordDict['KDA'] = playerKDA

    #计算击杀、死亡、助攻
    kdaStr = playerRecord.xpath('./td[2]/text()')[0]
    kdaStr = kdaStr.strip('\n')
    kdaStr = kdaStr.strip('\t')
    kill, death, assitance = kdaStr.split('/')
    playerRecordDict['Kill'] = kill
    playerRecordDict['Death'] = death
    playerRecordDict['Assitance'] = assitance

    #计算输出/参团率
    damageRate = playerRecord.xpath('./td[3]/p')[0].text
    playerRecordDict['DamageRate'] = damageRate
    teamContribute = playerRecord.xpath('./td[3]/text()')[0]
    playerRecordDict['TeamContribute'] = teamContribute.strip('\n').strip('\t')

    #经济/补刀
    farm = playerRecord.xpath('./td[4]/p')[0].text
    playerRecordDict['Farm'] = farm
    creeps = playerRecord.xpath('./td[4]/text()')[0].strip('\n').strip('\t')
    playerRecordDict['Creeps'] = creeps

    #插眼/排眼
    placeWard = playerRecord.xpath('./td[5]/p/text()')[0]
    playerRecordDict['PlaceWard'] = placeWard
    removeWard = playerRecord.xpath('./td[5]/text()')[0].strip('\n').strip('\t')
    playerRecordDict['RemoveWard'] = removeWard

    #装备和饰品
    items = playerRecord.xpath('./td[6]/div/img/@src')
    playerRecordDict['Items'] = items
    ornament = playerRecord.xpath('./td[6]/div/span/img/@src')[0]
    playerRecordDict['Ornament'] = ornament
    return playerRecordDict

#分析表格头 即提取队伍的输出、团队经济等等
def ExtractRecordTableHead(tableHead):
    #处理表格头，即提取退伍的输出、队伍经济、击杀数、视野占有率等等
    resultDict = {}

    headInfs = tableHead.xpath('./*')
    resultDict['Outcome'] = tableHead[1].text
    resultDict['TeamFarm'] = tableHead[2].xpath('./*')[0].text
    resultDict['TeamSlain'] = tableHead[3].xpath('./*')[0].text
    resultDict['VisualRate'] = tableHead[4].xpath('./*')[0].text

    return resultDict


#分析队伍信息
def GetTeamRecordDict(teamRecord, teamColor):
    #teamRecord 即contest-unfold 和 ~ unfold-defeated
    teamRecordDict = {}
    teamRecordDict['Color'] = teamColor
    #print 'teamRecord =', teamRecord.tag, teamRecord.attrib

    #表格头
    tableHead = teamRecord.xpath('./div[@class="unfold-hd"]')[0]
    teamRecordDict.update(ExtractRecordTableHead(tableHead))

    #提取队伍内每个玩家的信息
    playerRecords = []
    heros = teamRecord.xpath('./div[2]/table/tbody/tr')[1: 6]
    for hero in heros:
        playerRecords.append(ExtractPlayerRecord(hero))
    teamRecordDict['PlayerRecords'] = playerRecords
    return teamRecordDict

def AnalysisRecord(playerMatchUrl, playerName):
    #print 'Player', playerName, ',AnalysisRecord begining'

    local = CONF.HTML_PATH + playerName + '.html'
    try:
        urllib.urlretrieve(playerMatchUrl, local)
    except Exception, e:
        print 'Error when download player', playerName, 'record!'
        print e
        return

    tree = etree.HTML(open(local, 'r').read())

    #提取玩家信息
    playerInfDict = {}
    playerInfDict['PlayerName'] = tree.xpath('/html/body/div[3]/div/div[1]/div/div[1]/h6')[0].text
    playerInfDict['PersonalRating'] = tree.xpath('/html/body/div[3]/div/div[1]/div/div[1]/div[2]/span')[0].text
    playerInfDict['ServerName'] = tree.xpath('/html/body/div[3]/div/div[1]/div/div[1]/p/em')[0].text
    #print '玩家名称 ', playerInfDict['PlayerName'].encode('utf-8'),playerInfDict['PersonalRating'].encode('utf-8'), playerInfDict['ServerName'].encode('utf-8')

    #提取比赛信息
    matchRecords = []
    matchRecordsInf = tree.xpath('//div[@class="contest-list"]')
    for record in matchRecordsInf :
        recordDict = {}
        #分析蓝队
        blueRecordsDict = GetTeamRecordDict(record.xpath('./div[2]/div[1]')[0], 'blue')
        #OutputDictionary.DfsOutput(blueRecordsDict)
        #分析紫队
        purpleRecordDict = GetTeamRecordDict(record.xpath('./div[2]/div[2]')[0], 'purple')
        #OutputDictionary.DfsOutput(purpleRecordDict)
        recordDict['BlueRecordsDict'] = blueRecordsDict
        recordDict['PurpleRecordDict'] = purpleRecordDict
        matchRecords.append(recordDict)
    playerInfDict['MatchRecord'] = matchRecords

    return playerInfDict
