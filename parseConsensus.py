__author__ = 'Pratik'

import os
import sys

# read about stem library might be helpful

tempRelayMap = {}
finalRelayMap = {}
timeMap = {}
lines = []
relayCount = 0

def readConsensus(folderPath):
    path = ''
    global lines
    for date in os.listdir(folderPath):
        path = folderPath + '/' + date
        for file in os.listdir(path):
            with open(path + '/' + file, 'r') as consensusFile:
                lines = consensusFile.readlines()
                fromIndex = getConsensusStart(0)
                while fromIndex < len(lines):
                    nextIndex = getConsensusStart(fromIndex + 1)
                    if nextIndex > -1:
                        storeRelay(fromIndex, nextIndex)
                        fromIndex = nextIndex
                    else:
                        break
    print('count :' + str(relayCount))
    print('temp :' + str(len(tempRelayMap.keys())))


def getConsensusStart(fromIndex):
    global relayCount
    if fromIndex < len(lines):
        for index in range(fromIndex, len(lines)):
            if lines[index].startswith('r '):
                relayCount += 1
                return index
    return -1

def storeRelay(index, nextIndex):
    relayIp = ''
    relayType = -1
    time = ''
    global tempRelayMap
    if index > 0:
        while index < nextIndex:
            if (lines[index].startswith('r ')):
                relayIp = lines[index].split(' ')[6].strip()
                time = ' '.join(lines[index].split(' ')[4:6]).strip()
                timeMap[relayIp] = time
            elif (lines[index].startswith('s ')):
                relayType = getRelayType(lines[index])
            index += 1
        if relayType > 0:
            if relayIp not in tempRelayMap:
                tempRelayMap[relayIp] = [0, 0, 0]
            tempRelayMap[relayIp][relayType - 1] += 1


def getRelayType(line):
    type = 0
    isBadExit = False
    for linePart in line.split(' '):
        if linePart == 'Guard':
            type += 2
        elif linePart == 'Exit':
            type += 1
        elif linePart == 'BadExit':
            isBadExit = True

    if isBadExit and type > 2:
        type -= 1
    return type


def getFinalRelayTypes():
    for key in tempRelayMap.keys():
        types = tempRelayMap[key]
        if types[0] + types[2] > types[1] + types[2]:
            finalRelayMap[key] = 1
        else:
            finalRelayMap[key] = 2

def writeKeysForAsnLookup():
    global finalRelayMap
    outPath = 'E:/StudyStuff/Capstone/tools/torps_data/qq/keys.txt'
    timeOutPath = 'E:/StudyStuff/Capstone/tools/torps_data/qq/time.txt'

    with open(outPath, 'a+') as keysFile:
        keysFile.write('begin\nverbose\n')
        for key in finalRelayMap.keys():
            keysFile.write(key + '\n')
        keysFile.write('end')
    with open(timeOutPath, 'a+') as timeFile:
        timeFile.write('begin\nverbose\n')
        # for key in timeMap.keys():
        for key in finalRelayMap.keys():
            timeFile.write(key + ' ' + timeMap[key] + '\n')
        timeFile.write('end')

if __name__ == '__main__':
    folderPath = input('Enter consensus file path: ')
    readConsensus(folderPath)
    getFinalRelayTypes()
    writeKeysForAsnLookup()
    # ^r [a-zA-Z0-9 +-=]*\ns
    # E:\StudyStuff\Capstone\tools\torps_data\consensuses-2017-10