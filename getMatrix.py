__author__ = 'Pratik'

import sys
import copy

# def loadRelationFile(filename):
#     topology = {}
#     with open(filename,'r') as file:
#         for line in file:
#             if line.startswith('#'):
#                 continue
#             lineParts = line.split('|')
#             if len(lineParts) != 3:
#                 print("Invalid Topology")
#                 sys.exit(0)
#             fromAS = lineParts[0].strip()
#             toAS = lineParts[1].strip()
#             edgeType = int(lineParts[2].strip()) # -1: provider-customer; 0: peer-to-peer
#             if fromAS not in topology:
#                 topology[fromAS] = []
#             topology[fromAS].append(toAS)
#             if toAS not in topology:
#                 topology[toAS] = []
#             topology[toAS].append(fromAS)
#         print("Number of ASes: " + str(len(topology)))
#         return topology

#
# def loadRelationFile(filename):
#     topology = {}
#     with open(filename,'r') as file:
#         for line in file:
#             if line.startswith('#'):
#                 continue
#             lineParts = line.split('|')
#             if len(lineParts) != 3:
#                 print("Invalid Topology")
#                 sys.exit(0)
#             fromAS = lineParts[0].strip()
#             toAS = lineParts[1].strip()
#             edgeType = int(lineParts[2].strip()) # -1: provider-customer; 0: peer-to-peer
#             if fromAS not in topology:
#                 topology[fromAS] = [[], []]
#             topology[fromAS][edgeType+1].add(toAS)
#             if toAS not in topology:
#                 topology[toAS] = [[], []]
#             topology[toAS][edgeType + 1].add(fromAS)
#         print("Number of ASes: " + str(len(topology)))
#         return topology




def loadRelationFile(filename):
    topology = {}
    with open(filename,'r') as file:
        for line in file:
            if line.startswith('#'):
                continue
            lineParts = line.split('|')
            if len(lineParts) != 3:
                print("Invalid Topology")
                sys.exit(0)
            fromAS = lineParts[0].strip()
            toAS = lineParts[1].strip()
            edgeType = int(lineParts[2].strip()) # -1: provider-customer; 0: peer-to-peer
            if fromAS not in topology:
                topology[fromAS] = []
            topology[fromAS].append(toAS)
            if toAS not in topology:
                topology[toAS] = []
                if edgeType == 0:
                    topology[toAS].append(fromAS)
        print("Number of ASes: " + str(len(topology)))
        return topology




def getAllPaths(topology, source, dest):
    visited = set()
    paths = []
    currentPath = []
    allPathsDFS(topology, source, dest, visited, paths, currentPath)
    return paths

def allPathsDFS(topology, source, dest, visited, paths, currentPath):
        visited.add(source)
        currentPath.append(source)
        global count

        if source == dest:
            print(currentPath)
            paths.append(copy.copy(currentPath))
        else:
            # for asn in topology[source][0]:
            for asn in topology[source]:
                if asn not in visited:
                    allPathsDFS(topology, asn, dest, visited, paths, currentPath)
        currentPath.pop()
        visited.remove(source)


def getValues(exitASes, serverASes, suspectASes, allPaths):
    values = []
    for exitAS in exitASes:
        rowValue = []
        for suspectAS in suspectASes:
            exsersus = 0
            for serverAS in serverASes:
                paths = allPaths[exitAS][serverAS]
                occurance = 0
                for path in paths:
                    if suspectAS in path:
                        occurance += 1
                exsersus += occurance / len(paths)
            rowValue.append(exsersus / len(serverASes))
        values.append(rowValue)
    return values


if __name__ == '__main__':
    sys.setrecursionlimit(60000)
    # filename = input('Enter AS relation filepath: ')
    filename = './20171001.as-rel.txt'
    # exits = input('Enter list of exit ASes (comma separated values): ')
    exits = '3462,6830,8437,12389,12876,14061,20473,29998,31261,33920,34224,51167,62744,197922,201702'
    exitASes = exits.split(',')

    # servers = input('Enter list of server ASes (comma separated values): ')
    servers = '4808,14907,15169,16509,32934,36646,37963,54113,13414'
    serverASes = servers.split(',')

    # suspects = input('Enter list of suspect ASes (comma separated values): ')
    suspects = '3356,174,1299,2914,3257,6762,6453,6939,2828,1273'
    suspectASes = suspects.split(',')

    # read topology
    topology = loadRelationFile(filename)

    # with open('./topo.txt', 'a+') as topo:
    #     for key in topology.keys():
    #         topo.write('v ' + key + ' ' + key + '\n')
    #
    #     for key in topology.keys():
    #         rels = topology[key]
    #         for relation in rels[0]:
    #             topo.write('e ' + key + ' ' + relation + ' pc\n')
    #         for relation in rels[1]:
    #             topo.write('e ' + key + ' ' + relation + ' pp\n')
    #         for relation in rels[2]:
    #             topo.write('e ' + key + ' ' + relation + ' cp\n')



    # find all paths from exitAS to sererAS

    allPaths = {}

    for exitAS in exitASes:
        allPaths[exitAS] = dict()
        for serverAS in serverASes:
            paths = getAllPaths(topology, exitAS, serverAS)
            print('got paths for ' + exitAS + ' -> ' + serverAS)
            allPaths[exitAS][serverAS] = paths
    print('all paths done')

    for exitASN in allPaths.keys():
        print('AS: ' + exitASN)
        paths = allPaths[exitASN]
        for serverANS in paths.keys():
            print('server: ' + serverANS)
            with open('./path_' + str(exitASN) + '_' + str(serverANS), 'a+') as pathFile:
                for path in allPaths[exitASN][serverANS]:
                    pathFile.write('->'.join(path) + '\n')


    # get values
    # values = getValues(exitASes, serverASes, suspectASes, allPaths)
    # # print(values)
    # outputFile = './values.txt'
    # with open(outputFile, 'a+') as output:
    #     for row in values:
    #         for value in row:
    #             output.write(str(value) + ',')
    #         output.write('\n')



# E:\StudyStuff\Capstone\Papers\De_try\20171001.as-rel.txt
#
