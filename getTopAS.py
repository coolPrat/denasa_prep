__author__ = 'Pratik'

from os import listdir
import operator

ipToAsMap = {}
relayCount = {}

def getTopAS(filePath):
    count = 0
    asMap = {}
    with open(filePath, 'r+') as file:
        for line in file:
            count += 1
            if (count == 1):
                continue
            else:
                lineParts = line.split('|')
                asNumber = lineParts[0].strip()
                ip = lineParts[1].strip()
                if asNumber in asMap:
                    asMap[asNumber] += 1
                else:
                    asMap[asNumber] = 1

                if ip not in ipToAsMap:
                    ipToAsMap[ip] = asNumber
    separateRelays()
    return getTop10(asMap)


def getTop10(asMap):
    sortedASMap = sorted(asMap.items(), key=operator.itemgetter(1), reverse=True)
    top10AS = []
    count = 0
    print(sortedASMap)
    for key in sortedASMap:
        if count < 10:
            top10AS.append(key)
            count += 1
        else:
            break
    return top10AS


def separateRelays(consensusesFile):
    nums = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10']
    for i in nums:
        fileList = listdir(consensusesFile + '/' + i)
        for file in fileList:
            with open(consensusesFile + '/' + i + '/' + file, 'r+') as consFile:
                relay = ''
                type = ''
                for line in consFile:
                    if line.startswith('r '):
                        relay = newRelay(line)
                    elif line.startswith('s '):
                        type = getType(line)
                        ipToAsMap[]


def newRelay(line):
    return line.split(' ')[6].strip()

def getType(line):
    if ' Exit ' in line:
        return 'exit'
    elif ' Guard ' in line:
        return 'guard'


if __name__ == '__main__':
    ipToAsFile = input('Enter path to IP-AS mapping file: ')
    topAS = getTopAS(ipToAsFile)
    print(topAS)
    consensusesFile = input('Enter path to consensuses-files: ')
    separateRelays(consensusesFile)
