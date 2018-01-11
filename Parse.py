#! /usr/bin/python3
import sys
import re

def seperateTablets(filename):
    tabletStrings = []
    tabFile = open(filename, 'r')
    curText = []
    curId = ""
    for line in tabFile:
        if(line[0] == '&'):
            if curId:
                tabletStrings.append((curId, curText))
            curId = line.strip()
            curText = []
        else:
            curText.append( line.strip() )
    return tabletStrings

def parseId(dict, idLine):
    match = re.search('&W+ = *+, W+' , idLine) # Ehhh????

def parseText(dict, text):



def parseTablet(tabletText):
    tablet = {}
    parseId(tablet, tabletText[0])
    parseText(tablet, tabletText[1])
    return tablet


def main(filename):
    tabletStrings = seperateTablets(filename)
    print(tabletStrings[0])

if __name__ == "__main__":
    main(sys.argv[1])
