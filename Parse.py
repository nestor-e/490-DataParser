#! /usr/bin/python3
import sys
import re


# In memory tablet representation, JSON-like structure
#  {IdToken1 : String, IdToken2 : String, IdToken3 : String,
#      Sides : [{side : Left/Right/Obverse/Reverse,
#                Content : [{subregion : none/seal/column/..., regionNum : n (optional), lines : [Line 1 (String), Line 2 (String), ...]},
#           ... ]},
# ...] }


# Determines if a section header denotes a side or not, this list may need to be expanded
def isSideMarker(string):
    return string in ["@obverse", "@reverse", "@left", "@right", "@top", "@botttom"]

# Tablets are delineated by lines begining with &
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
            if len(line.strip()) > 0 and line[0] not in "#$":  # Ignore comments and empty lines
                curText.append( line.strip() )
    return tabletStrings


# Construct representation of tablet from associated lines in file, if possible
def parseTablet(tabletText):
    tablet = {}
    if parseId(tablet, tabletText[0]) and parseText(tablet, tabletText[1]):
        return tablet
    else:
        return None

# First line in file for each tablet contains Id in format &Pxxxxxx = SomeString, AnotherString
# I dont know what exactly these represent so I grab all three parts
def parseId(d, idLine):
    match = re.search(r'^&(\w+) = (.+?), (.+)' , idLine)
    if match:
        d['IdToken1'] = match.group(1)
        d['IdToken2'] = match.group(2)
        d['IdToken3'] = match.group(3)
        return True
    else:
        return False

# Contents of each tablet devided into sections, delineated by lines begining with @
# these seem to have some nested structure but it's not clear how exactly that is defined
# the following methods represent my best guess
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

# Outer most nested layer is labeled by a fixed set of section names corrosponding
# to sides of the tablet as determined by isSideMarker function
def readSide(lines, start):
    side = {}
    end = start + 1
    while end < len(lines) and not isSideMarker(lines[end]):
        end += 1
    side['side'] = lines[start][1:]
    side['content'] = []
    start += 1
    while start < end:
        (elem, start) = parseRegion(lines, start, end)
        side['content'].append(elem)
    return (side, end)



def parseRegion(lines, start, end):
    region  = {}
    region['subregion']  = "none"
    region['lines'] = []
    cur = start
    if lines[start][0] == '@':
        cur += 1
        m = re.search(r"^@(\w+) ?(\d*)", lines[start])
        if m:
            region['subregion']  = m.group(1)
            if m.group(2):
                region['regionNum'] = m.group(2)

    while cur < end and lines[cur][0] != '@':
        #TODO: decide what lines like >>Qxxxxxxx nnn mean, I dont think they are text
        m = re.match(r"^[0-9.']+ ?(.+)", lines[cur]) # to exclude such lines
        #m = re.match(r"^[0-9.'>]+ ?(.+)", lines[cur]) # to include them
        if m:
            region['lines'].append(m.group(1))
        cur += 1
    return (region, cur)




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
