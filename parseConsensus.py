__author__ = 'Pratik'

import os
import sys

# read about stem library might be helpful

tempRelayMap = {}
# finalRelayMap = {}
finalRelayMap = {1: set(), 2: set()}
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
            finalRelayMap[1].add(key)
            # finalRelayMap[key] = 1
        else:
            finalRelayMap[2].add(key)
            # finalRelayMap[key] = 2

def writeKeysForAsnLookup():
    global finalRelayMap
    outPath = './output/keys.txt'
    timeOutPath = './output/time.txt'

    # with open(outPath, 'a+') as keysFile:
    #     keysFile.write('begin\nverbose\n')
    #     for key in finalRelayMap.keys():
    #         keysFile.write(key + '\n')
    #     keysFile.write('end')
    # with open(timeOutPath, 'a+') as timeFile:
    #     timeFile.write('begin\nverbose\n')
    #     # for key in timeMap.keys():
    #     for key in finalRelayMap.keys():
    #         timeFile.write(key + ' ' + timeMap[key] + '\n')
    #     timeFile.write('end')

    with open(outPath, 'a+') as keysFile:
        keysFile.write('begin\nverbose\n')
        for key in finalRelayMap[1]:
            keysFile.write(key + '\n')
        keysFile.write('end')


def getServerIps(filepath):
    lines = []
    with open(filepath, 'r+') as serverFile:
        lines = serverFile.readlines()
    with open('./output/serverIps.txt', 'a+') as serverIpsFile:
        serverIpsFile.write('begin\nverbose\n')
        for line in lines:
            serverIpsFile.write(line.split(',')[-1].strip() + '\n')
        serverIpsFile.write('end')


def checkAllIps():
    keys = []
    keys_resolved = []
    ases = set()
    with open('./output/keys.txt', 'r+') as keysFile:
        keys = keysFile.readlines()
    with open('./output/keys_resolved.txt', 'r+') as keysResolvedFile:
        keys_resolved = keysResolvedFile.readlines()

    keys_set = set()
    for key in keys:
        keys_set.add(key.strip())

    for resolved_key in keys_resolved[1:]:
        ip = resolved_key.split('|')[1].strip()
        if ip not in keys_set:
            print(ip)
            # keys_set.remove(ip)
        else:
            ases.add(resolved_key.split('|')[0].strip())
    print('Number of exit ASes: ' + str(len(ases)))
    with open('./output/exitASes.txt', 'a+') as exitASes:
        exitASes.write(','.join(ases))

def getAllServers():
    keys = []
    servers_resolved = []
    ases = set()
    servers = set()
    with open('./output/servers_resolved.txt', 'r+') as keysResolvedFile:
        servers_resolved = keysResolvedFile.readlines()

    for server in servers_resolved[1:]:
        asn = server.split('|')[0].strip()
        ip = server.split('|')[1].strip()
        servers.add(ip)
        ases.add(asn)

    print('Number of servers: ' + str(len(servers)))
    print('Number of ASes for servers: ' + str(len(ases)))

    with open('./output/destinations.txt', 'a+') as unique_server:
        unique_server.write(','.join(servers))
        # for server in servers:
        #     unique_server.write(server + ',')



if __name__ == '__main__':
    # folderPath = input('Enter consensus file path: ')
    # readConsensus(folderPath)
    # getFinalRelayTypes()
    # writeKeysForAsnLookup()

    # serverPath = input('Enter server ip file path: ')
    # getServerIps(serverPath)


    # checkAllIps()

    getAllServers()




    # ^r [a-zA-Z0-9 +-=]*\ns
    # E:\StudyStuff\Capstone\tools\torps_data\consensuses-2017-10
    # /media/pratik/New Volume/StudyStuff/Capstone/tools/torps_data/consensuses-2017-10
    # /media/pratik/New Volume/StudyStuff/Capstone/tools/torps_data/qq/alexa-top-1000-ips (copy).csv

    #  verifying new code -> it works!
    # ips = set()
    # with open('./output/keys_old_2.txt', 'r+') as oldFile:
    #     ipList = oldFile.readlines()
    #     for ip in ipList:
    #         if ip not in ips:
    #             ips.add(ip)
    # print(len(ips))