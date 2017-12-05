import requests
import json
from bs4 import BeautifulSoup
from html.parser import HTMLParser
import copy

visited = set()
paths = []
currentPath = []

def getAllPaths(exitASes, servers):
    global paths
    url = "https://www.bgpvista.com/asinfer.php"
    delimiter = '\r\n'
    startToken = '------WebKitFormBoundary7MA4YWxkTrZu0gW'
    content_type = 'Content-Disposition: form-data; '
    headerString = startToken + delimiter + content_type
    source_part = 'name="SRCASN"' + delimiter + delimiter + '%s' + delimiter
    destination_part = 'name="DSTPREFIX"' + delimiter + delimiter + '%s' + delimiter
    payload1 = headerString + source_part + headerString + destination_part + startToken + '--'


    for exitAS in exitASes:
        for server in servers:
                payload2 = payload1 % ('AS' + exitAS, server.strip())
                headers = {
                    'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW"
                }

                response = requests.request("POST", url, data=payload2, headers=headers)
                # print(response.text)

                htmlDom = BeautifulSoup(response.text)
                try:
                    if htmlDom.find_all('script')[1].contents[0].startswith('var graph'):
                        scriptObj = json.loads(htmlDom.find_all('script')[1].contents[0].split('=')[1][:-1])
                        getPaths(scriptObj)
                        with open('./output/paths/path_' + str(exitAS) + '_' + str(server), 'a+') as pathFile:
                            for path in paths:
                                pathFile.write('->'.join(path) + '\n')
                        paths = []
                except Exception as e:
                    with open('./output/paths/path_' + str(exitAS) + '_' + str(server), 'a+') as pathFile:
                        pathFile.write('')



def getPaths(graph):
    vertices = []
    source = ''
    destination = ''
    for node in graph['nodes']:
        vertices.append(node['name'])
        if node['group'] == 5:
            source = node['name']
        elif node['group'] == 2:
            destination = node['name']

    edges = dict()
    for edge in graph['links']:
        if vertices[edge['source']] not in edges:
            edges[vertices[edge['source']]] = set()
        edges[vertices[edge['source']]].add(vertices[edge['target']])

    allPathsDFS(edges, source, destination)
    # with open('./output/paths/path_' + str(source) + '_' + str(destination), 'a+') as pathFile:
    #     for path in paths:
    #         pathFile.write('->'.join(path) + '\n')


def allPathsDFS(edges, source, destination):
    visited.add(source)
    currentPath.append(source)
    if source == destination:
        # print(currentPath)
        paths.append(copy.copy(currentPath))
        # with open('./output/paths/path_' + str(source) + '_' + str(destination), 'a+') as pathFile:
        #     pathFile.write('->'.join(currentPath) + '\n\n')
    else:
        # for asn in topology[source][0]:
        for asn in edges[source]:
            if asn not in visited:
                allPathsDFS(edges, asn, destination)
    currentPath.pop()
    visited.remove(source)

def getValues(exitASes, servers, suspectASes, allPathsFile):
    values = {}
    for exitAS in exitASes:
        rowValue = {}
        for server in servers:
            with open(allPathsFile + '/path_' + exitAS + '_' + server) as serverPath:
                paths = serverPath.readlines()
                for suspectAS in suspectASes:
                    occurance = 0
                    for path in paths:
                        if suspectAS in path:
                            occurance += 1
                    if suspectAS not in rowValue:
                        rowValue[suspectAS] = 0
                    if len(paths) > 0:
                        rowValue[suspectAS] += occurance / len(paths)
        for key in rowValue.keys():
            rowValue[key] = rowValue[key] / len(servers)
        values[exitAS] = rowValue
    return values


def writeValues(values, count):
    with open('./output/values/posibilities_' + str(count) + '.txt', 'a+') as posibilities:
        for key in values.keys():
            for key2 in values[key]:
                posibilities.write(key + ',' + key2 + ',' + str(values[key][key2]) + '\n')


if __name__ == '__main__':

    exitASes = []
    serversList = []
    exitPath = input('Enter path of exit ASes: ')
    exits = open(exitPath, 'r+').readlines()
    if len(exits) != 1:
        print('Invalid exitAS file')
    else:
        exitASes = exits[0].split(',')

    serverPath = input('Enter path of servers: ')
    servers = open(serverPath, 'r+').readlines()
    if len(servers) != 1:
        print('Invalid servers file')
    else:
        serversList = servers[0].split(',')

    suspects = input('Enter the list of suspect ASes')
    suspectASes = suspects.split(',')

    count = input('Enter count: ')

    getAllPaths(exitASes, serversList)

    values = getValues(exitASes, serversList, suspectASes, './output/paths')
    writeValues(values, count)

    # i = 0
    # count = 1
    # while i < len(exitASes):
    #     with open('./output/exitASes_' + str(count) + '.txt', 'a+') as dest:
    #         dest.write(','.join(exitASes[i:i+65]))
    #     i += 65
    #     count += 1



#     ./output/exitASes_3.txt
#     ./output/destinations.txt
#     3356,174,1299,2914,3257,6762,6453,6939,2828,1273
