#! /usr/bin/python3
import sys
import re


# In memory tablet representation, JSON-like structure
# {   idCDLI : String, idName : String,
#     objectType : String, startsOn : int, endsOn : int,
#     sides : [
#         {   side : None, Left/Right/Obverse/Reverse/...,
#             content : [
#                 {   subregion : none/seal/column/...,
#                     regionNum : n (optional),
#                     lines : [ {text : String, comments : String[] , attestations : [word]} , ... ]
#                 }, ...
#             ]
#         }, ...
#     ]
#  }


# Tentative list of special tokens in file format
CDLI_SIDE_LABELS  = ["@obverse", "@reverse", "@left", "@right", "@top", "@botttom", "@face", "@surface"] ## Array in vs String in
CDLI_OBJECT_TYPES = ["@tablet","@envelope","@prism","@bulla","@fragment","@object"]
CDLI_COMMENT_MARKERS = ['#', '$', '>']

#Compile regular expressions relating to various parts of ATF file
REGEX_ID = re.compile(r'^&(\w+) = (.+)')
REGEX_REGION_START = re.compile(r"^@(\w+) ?(\d*)")
REGEX_LINE_START = re.compile(r"^[0-9.']+ ?(.+)")
REGEX_LINE_CONTINUE = re.compile(r"^ (.+)")
# REGEX_LINE_REFRENCE = re.compile(r"^>>(\w+) ([\w']+)")

# Determines if a section header denotes a side or not, this list may need to be expanded
def isSideMarker(string):
    return string in CDLI_SIDE_LABELS

# Tablets are delineated by lines begining with &
def seperateTablets(filename):
    tabletStrings = []
    tabFile = open(filename, 'r', encoding='utf-8')
    curText = []
    curId = ""
    curLineStart = 0
    lineNum = 0
    for line in tabFile:
        if(line[0] == '&'):
            if curId:
                tabletStrings.append((curId, curText, (curLineStart, lineNum - 1)))
            curId = line.strip()
            curText = []
            curLineStart = lineNum
        else:
            if len(line.strip()) > 0:  # Ignore empty lines
                curText.append( line.strip() )
        lineNum += 1
    return tabletStrings


# Construct representation of tablet from associated lines in file, if possible
def parseTablet(tabletText):
    tablet = {}
    if parseId(tablet, tabletText[0]) and parseText(tablet, tabletText[1]):
        tablet['startsOn'] = tabletText[2][0]
        tablet['endsOn'] = tabletText[2][1]
        return tablet
    else:
        return None

# First line in file for each tablet contains Id in format &Pxxxxxx = SomeString, AnotherString
# I dont know what exactly these represent so I grab all three parts
def parseId(d, idLine):
    match = REGEX_ID.match(idLine)
    if match:
        d['idCDLI'] = match.group(1)
        d['idName'] = match.group(2)
        return True
    else:
        return False

# Contents of each tablet devided into sections, delineated by lines begining with @
# these seem to have some nested structure but it's not clear how exactly that is defined
# the following methods represent my best guess
def parseText(d, text):
    if len(text) == 0:
        return False
    else:
        i = 0
        while text[i][0] in CDLI_COMMENT_MARKERS:
            i+=1
        if text[i] in CDLI_OBJECT_TYPES:
            d['objectType'] = text[i][1:]
            i  += 1
        else:
            d['objectType'] = 'None'
        sides = []
        while i < len(text):
            (side, i) = readSide(text, i)
            sides.append(side)
        d['sides'] = sides
        return True

# Outer most nested layer is labeled by a fixed set of section names corrosponding
# to sides of the tablet as determined by isSideMarker function
def readSide(lines, start):
    side = {}
    end = start + 1
    while end < len(lines) and not isSideMarker(lines[end]):
        end += 1
    if isSideMarker(lines[start]):
        side['side'] = lines[start][1:]
        start += 1
    else:
        side['side'] = 'none'
    side['content'] = []
    while start < end:
        (elem, start) = parseRegion(lines, start, end)
        side['content'].append(elem)
    return (side, end)


# Actual text content of tablets is contained in contiguos regions of the file
# I am calling subregions.  Each subregion begins with a line:
# @(label) (index)
# where label can be any string, and the index(optional) is the running count of
# that particular label within the current side
def parseRegion(lines, start, end):
    region  = {}
    region['subregion']  = "none"
    region['lines'] = []
    cur = start
    if lines[start][0] == '@':
        cur += 1
        m = REGEX_REGION_START.search(lines[start])
        if m:
            region['subregion']  = m.group(1)
            if m.group(2):
                region['regionNum'] = m.group(2)

    while cur < end and lines[cur][0] != '@':
        (lineRecord, cur) = parseLine(lines, cur, end)
        if(lineRecord):
            region['lines'].append(lineRecord)
    return (region, cur)

def parseLine(lines, start, end):
    cur = start
    lineMatch = REGEX_LINE_START.match(lines[cur])
    if lineMatch:
        lineRecord = {}
        lineRecord['text'] = lineMatch.group(1)
        cur += 1
        cont = True
        while cur < end and cont:
            continueMatch = REGEX_LINE_CONTINUE.match(lines[cur])
            if continueMatch:
                lineRecord['text'].append(continueMatch.group(1))
                cur += 1
            elif lines[cur][0] in CDLI_COMMENT_MARKERS:
                if 'comments' not in lineRecord:
                    lineRecord['comments'] = []
                lineRecord['comments'].append(lines[cur])
                cur += 1
            else :
                cont = False
        return (lineRecord, cur)
    else:
        return (None, start + 1)

# I don't understand how this is possible but there are some tablets in the atf file with the same Id
def cleanDuplicateIds(data):
    ids = set()
    for tab in data:
        tId = tab['idCDLI']
        while tId in ids:
            tId += tab['idName']
        tab['idCDLI'] = tId
        ids.add(tId)

# Prints whole text of a tablet in order it appears in file, without annotation
# Demo of how to traverse data structure
def getFullText(tablet):
    text  = ""
    for side in tablet['sides']:
        for region in side['content']:
            for line in region['lines']:
                text += line['text'] + "\n"
    return text


# Reads all records that look like tablets from given file
def getTabletsFromFile(filename):
    tabletStrings = seperateTablets(filename)
    tablets = []
    for t in tabletStrings:
        temp = parseTablet(t)
        if temp != None:
            tablets.append(temp)
    cleanDuplicateIds(tablets)
    return tablets


def main(filename):
    tablets = getTabletsFromFile(filename)
    print(tablets[0])

if __name__ == "__main__":
    main(sys.argv[1])
