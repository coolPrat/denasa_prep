__author__ = 'Pratik'

from os import listdir
from os import path


ipFile = 'E://StudyStuff//Capstone//tools//torps_data//server_ips_2017_10.txt'
bandwidthFile = 'E://StudyStuff//Capstone//tools//torps_data//server_bandwidth_2017_10.txt'

ipMap = {}

def writeIps(ipList):
    with open(ipFile, 'a+') as output:
        output.write('\n'.join(ipList))


def writeBandwidth(bandwidthList):
    with open(bandwidthFile, 'a+') as bandwidth:
        bandwidth.write('\n'.join(bandwidthList))


def readDescriptors(folderPath):
    count = 0
    totalCount = 0
    errorCount = 0
    ipList = ['begin', 'verbose']
    bandwidthList = []

    for dir1 in listdir(folderPath):
        for dir2 in listdir(folderPath + '/' + dir1 ):
            fileList = listdir(folderPath + '/' + dir1 + '/' + dir2)
            for file in fileList:
                if path.isfile(folderPath + '/' + dir1 + '/' + dir2 + '/' + file):
                    ip = ''
                    time = ''
                    with open(folderPath + '/' + dir1 + '/' + dir2 + '/' + file) as descriptor:
                        propertyCount = 0
                        try:
                            for line in descriptor:
                                if line.startswith('router '):
                                    ip = line.split(' ')[2]
                                    propertyCount = 3
                                    ipMap[ip] = 1
                                    # propertyCount += 1
                                # elif line.startswith('published '):
                                #     time = ' '.join(line.strip().split(' ')[1:]) + ' GMT'
                                #     propertyCount += 1
                                # elif line.startswith('bandwidth '):
                                #     tempList = line.strip().split(' ')[1:]
                                #     tempList.insert(0, ip)
                                #     bandwidthList.append(','.join(tempList))
                                #     propertyCount += 1

                                if propertyCount == 3:
                                    # ipList.append(ip + ' ' + time)
                                    ipList.append(ip)
                                    count += 1
                                    if count == 10000:
                                        totalCount += count
                                        # writeIps(ipList)
                                        # writeBandwidth(bandwidthList)
                                        # ipList = list()
                                        # bandwidthList = list()
                                        count = 0
                                        print(str(totalCount) + ' Done!')
                                    break
                        except Exception as e:
                            errorCount += 1
                            print('error in : ' + file)
                            continue
    ipList.append('end')
    totalCount += count
    print('final count: ' + str(len(ipMap.keys())))
    # writeIps(ipList)




if __name__ == '__main__':
    folderPath = input("Enter folder path to server descriptors: ")
    readDescriptors(folderPath)



