#!/usr/bin/python3

#  Associates line numbers with the tablet Id's they are part of using binary search

import Parse
import csv
import sys

class LineFinder:
    def __init__(self, data):
        self.tabList = sorted( data, key= lambda tab: tab['startsOn'] )

    def find(self, lineNum, expectedName = None):
        q = 0;
        r  = len(self.tabList)
        found = None
        while q < r:
            mid = (q + r) // 2
            midTab = self.tabList[mid]
            if midTab['startsOn'] > lineNum:
                r = mid
            elif midTab['endsOn'] < lineNum:
                q = mid + 1
            else:
                q = r
                found = midTab
        if found != None and expectedName != None:
            text = Parse.getFullText(found)
            if expectedName not in text:
                found = None
        return found

def makeAttestationMap(lf, nameFile):
    nameId = 1
    attest = []
    names = {}
    e = 0
    with open(nameFile) as nameF:
        reader = csv.DictReader(nameF)
        for line in reader:
            name = line['name']
            lineNum = int(line['lineid'])
            tab = lf.find(lineNum, name)
            if tab == None:
                #print("Warning:", name , " not found on line", lineNum)
                e += 1
            else:
                if name not in names:
                    names[name] = 'N{:06d}'.format(nameId)
                    nameId += 1
                attest.append( (tab['idCDLI'] , names[name]) )
    return (attest, names, e)



def main():
    try:
        tabFile = sys.argv[1]
    except IndexError:
        tabFile = 'cdliatf_unblocked.atf'

    try:
        nameFile = sys.argv[2]
    except IndexError:
        nameFile = 'output.csv'

    d = Parse.getTabletsFromFile(tabFile)
    f = LineFinder(d)
    del d
    (a, m, e) = makeAttestationMap(f, nameFile)
    print(len(a), 'attestations')
    print(e, 'not found')
    print(len(m), 'names')


if __name__ == '__main__':
    main()
