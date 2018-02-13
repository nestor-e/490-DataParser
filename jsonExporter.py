#!/usr/bin/python3
import sys
import Parse
import json


TEXT_ONLY_NAME = "CDLI_text.json"
FULL_NAME = "CDLI_full.json"


# Outputs full tablet representation for each tablet in toExport into new file (filename)
# formated in JSON
def jsonOutputFull(toExport, filename):
    f = open(filename, 'w')
    json.dump(toExport, f, indent=2)
    f.close()

# Outputs a map from TabletId -> TabletText for all tablets in toExport into given file
# formated in JSON
def jsonOutputTextOnly(toExport, filename):
    l = []
    for tab in toExport:
        d = {}
        d['id'] = tab['idCDLI']
        d['text'] = Parse.getFullText(tab)
        l.append(d)
    f = open(filename, 'w')
    json.dump(l, f)
    f.close()

def failMessage():
    print("Usage: python3 jsonExporter.py [CDLI data file] [Also export full structure: y/n]")


def main(args):
    if len(args) < 2 or len(args) > 3:
        failMessage()
    else:
        exists = False
        try:
            f = open(args[1], 'r')
            f.close()
            exists = True
        except FileNotFoundError:
            failMessage()

        if exists:
            tabs = Parse.getTabletsFromFile(args[1])
            jsonOutputTextOnly(tabs, TEXT_ONLY_NAME)
            if len(args) == 3 and args[2].lower() == 'y':
                jsonOutputFull(tabs, FULL_NAME)


if __name__ == "__main__":
    main(sys.argv)
