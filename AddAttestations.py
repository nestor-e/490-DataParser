#!/usr/bin/python3

#  Associates line numbers with the tablet Id's they are part of using binary search

import Parse
import jsonExporter
import csv
import sys
import re

Commas = re.compile(r",")

# # # CHANGE THESE TO REFLECT LOCATION OF SNER # # # # # # # # # # #
sys.path.append('../') ## PARENT DIRECTORY OF SNER (I'm not sure why this is nesccicary)
sys.path.append('../sner') ## SNER DIRECTORY
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


from sner.classes import Display
from sner.scripts import utilities



def cleanLine(line):
    clean = utilities.clean_line(line.lower(), True, True).split()
    return clean

def find(data, lineNum):
    q = 0;
    r  = len(data)
    found = None
    while q < r:
        mid = (q + r) // 2
        midTab = data[mid]
        if midTab['startsOn'] > lineNum:
            r = mid
        elif midTab['endsOn'] < lineNum:
            q = mid + 1
        else:
            q = r
            found = midTab
    return found

def mapWords(data):
    # {word(clean) : [(TabId, sideIdx, regionIdx, lineIdx) ]}
    wordMap = {}
    dataPoints = len(data)
    disp = Display()
    disp.start('Mapping words in atf...')
    i = 0
    for tablet in data:
        for sideNum in range(len(tablet['sides'])):
            side = tablet['sides'][sideNum]
            for regionNum in range(len(side['content'])):
                region = side['content'][regionNum]
                for lineNum in range(len(region['lines'])):
                    line = region['lines'][lineNum]
                    clean = cleanLine(line['text'])
                    for word in clean:
                        if word not in wordMap:
                            wordMap[word] = []
                        wordRecord = (tablet['idCDLI'], sideNum, regionNum, lineNum)
                        wordMap[word].append(wordRecord)
        i += 1
        disp.update_progress_bar(i, dataPoints)
    disp.finish()
    return wordMap

def getNames(keyFile, resultFile):
    # {name : {id: String  on : [locations]}}
    names = {}
    idx = 1
    print('Reading names from sner results...')
    with open(keyFile, 'r') as k:
        with open(resultFile, 'r') as r:
            for kLine in k:
                isName = r.readline().strip() == '1'
                if isName:
                    kVals = kLine.split('\t')
                    word = kVals[3].strip()
                    lineNum = int( kVals[1].strip() )
                    if word not in names:
                        names[word] = {}
                        names[word]['id'] = 'N{:08d}'.format(idx)
                        names[word]['on'] = []
                        idx += 1
                    names[word]['on'].append(lineNum)
    print('Done')
    return names

def outputNames(names, filepath):
    with open(filepath, 'w') as out:
        write = csv.DictWriter(out, ['Name Id', 'Name' , 'Occurance Count'])
        write.writeheader()
        for name in names:
            write.writerow({'Name Id':names[name]['id'],
                            'Name' : Commas.sub(name, '.') ,
                            'Occurance Count' : len(names[name]['on'])})

def addAttestation(tablet, sideN, regionN, lineN, Id):
    side = tablet['sides'][sideN]
    region = side['content'][regionN]
    line = region['lines'][lineN]
    if 'attestations' not in line:
        line['attestations'] = []
    if Id not in line['attestations']:
        line['attestations'].append(Id)


def main(atfFile, keyFile, resultFile, outFileNames, outFileData):
    print("Parseing atf...  ")
    data = Parse.getTabletsFromFile(atfFile);
    data = sorted( data, key= lambda tab: tab['startsOn'] )
    print("Done.")
    words = mapWords(data)
    names = getNames(keyFile, resultFile)

    missedNames = 0
    missedLinks = 0
    print("Locating names in word map...")
    for name in names:
        if name in words:
            occurances = words[name]
            for location in names[name]['on']:
                tab = find(data, location)
                if tab == None:
                    print('Thing on line', location, 'of atf file not parsed as tablet')
                else:
                    tId = tab['idCDLI']
                    found = False
                    for i in occurances:
                        if i[0] == tId:
                            addAttestation(tab, i[1], i[2], i[3], names[name]['id'])
                            found = True
                    if not found:
                        missedLinks += 1
        else:
            missedLinks += len(names[name]['on'])
            missedNames += 1

    print("Done.  Lost {} names and {} links in translation.".format(missedNames, missedLinks))
    print("Creating output...")
    outputNames(names, outFileNames)
    jsonExporter.jsonOutputFull(data, outFileData)
    print("Done.")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
