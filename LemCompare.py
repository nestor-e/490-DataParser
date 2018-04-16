import csv
import sys


def loadLemmata(lemmataFile):
    pn = set()
    gn = set()
    other = set()
    with open(lemmataFile, 'r') as input:
        read = csv.reader(input, delimiter='\t')
        for row in read:
            if row[2] == 'PN':
                pn.add(row[1])
            elif row[2] == 'GN':
                gn.add(row[1])
            else:
                other.add(row[1])
    return (pn, gn, other)


def loadNames(namesFile):
    names = set()
    with open(namesFile, 'r') as input:
        read = csv.reader(input)
        for row in read:
            names.add(row[1])
    return names

def matchCount(names, lemPN, lemGN, lemOTHER):
    (matchPN, matchGN, matchOTHER, matchMulti, matchNONE) = (0, 0, 0, 0, 0)
    for name in names:
        matchCount = 0
        if name in lemPN:
            matchPN    += 1
            matchCount += 1
        if name in lemGN:
            matchGN    += 1
            matchCount += 1
        if name in lemOTHER:
            matchOTHER += 1
            matchCount += 1
        if matchCount > 1:
            matchMulti += 1
        elif matchCount < 1:
            matchNONE += 1
    return (matchPN, matchGN, matchOTHER, matchMulti, matchNONE)


def main(nameFile, lemFile):
    (pnSet, gnSet, otherSet) = loadLemmata(lemFile)
    names = loadNames(nameFile)
    (pn, gn, other, mult, none) = matchCount(names, pnSet, gnSet, otherSet)
    print('PN match : {}/{}'.format(pn, len(names)))
    print('GN match : {}/{}'.format(gn, len(names)))
    print('OTHER match : {}/{}'.format(other, len(names)))
    print('NONE match : {}/{}'.format(none, len(names)))
    print('Mulitple match : {}/{}'.format(mult, len(names)))

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
