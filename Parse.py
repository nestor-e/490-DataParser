#! /usr/bin/python3
import sys
import re


# In memory tablet representation, JSON-like structure
#  {IdToken1 : String, IdToken2 : String, IdToken3 : String,
#      Sides : [{Side : Left/Right/Obverse/Reverse,
#                Content : [{Subregion : None/Seal/Column, regionNum : n (optional), Lines : [Line 1, Line 2, ...]},
#           ... ]},
# ...] }

def isSideMarker(string):
    return string in "@obverse@reverse@left@right@top@botttom"

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
            if len(line.strip()) > 0 and line[0] not in "#$":  #Ignore comment lines
                curText.append( line.strip() )
    return tabletStrings


def parseRegion(lines, start, end):
    region  = {}
    region['subregion']  = "none"
    region['Lines'] = []
    cur = start
    if lines[start][0] == '@':
        cur += 1
        m = re.search(r"^@(\w+) ?(\d*)", lines[start])
        if m:
            region['subregion']  = m.group(1)
            if m.group(2):
                region['regionNum'] = m.group(2)

    while cur < end and lines[cur][0] != '@':
        m = re.match(r"^[0-9.'>]+ ?(.+)", lines[cur])
        #TODO: decide what lines like >>Qxxxxxxx nnn mean
        if m:
            region['Lines'].append(m.group(1))
        cur += 1
    return (region, cur)


def readSide(lines, start):
    side = {}
    end = start + 1
    while end < len(lines) and not isSideMarker(lines[end]):
        end += 1
    side['Side'] = lines[start][1:]
    side['Content'] = []
    start += 1
    while start < end:
        (elem, start) = parseRegion(lines, start, end)
        side['Content'].append(elem)
    return (side, end)



def parseId(d, idLine):
    match = re.search(r'^&(\w+) = (.+?), (.+)' , idLine)
    if match:
        d['IdToken1'] = match.group(1)
        d['IdToken2'] = match.group(2)
        d['IdToken3'] = match.group(3)
        return True
    else:
        return False

def parseText(d, text):
    if len(text) == 0 or text[0] != '@tablet':
        return False
    else:
        sides = []
        i  = 1
        while i < len(text):
            (side, i) = readSide(text, i)
            sides.append(side)
        d['sides'] = sides
        return True


def parseTablet(tabletText):
    tablet = {}
    if parseId(tablet, tabletText[0]) and parseText(tablet, tabletText[1]):
        return tablet
    else:
        return None


def main(filename):
    tabletStrings = seperateTablets(filename)
    tablets = []
    for t in tabletStrings:
        temp = parseTablet(t)
        if temp != None:
            tablets.append(temp)
    print(tablets[1])

if __name__ == "__main__":
    main(sys.argv[1])
