import os
import re
import csv


obj = re.compile(r'<li class="level1"><div class="li"> (\d+): ([^:\s]+): (.*)')
#<li class="level1"><div class="li"> 97: iti-bi: itud[moon]: <strong>iti[month]</strong></div>

def parseFile(handle):
    found = []
    for line in handle:
        q = obj.match(line)
        if q:
            count = q.group(1)
            standardForm = q.group(2)
            annotation = q.group(3)
            if '@PN' in annotation:
                found.append((count, standardForm, 'PN'))
            elif '@GN' in annotation:
                found.append((count, standardForm, 'GN'))
            else:
                found.append((count, standardForm, 'OTHER'))
    return found;


def main(path):
    lemmata = []
    for filename in os.listdir(path):
        if filename[-5:] == '.html':
            with open(path + '/' + filename, 'r') as src:
                lemmata += parseFile(src)
    with open('lemmata.csv', 'w') as out:
        wr = csv.writer(out, delimiter='\t', lineterminator='\n')
        for lem in lemmata:
            wr.writerow(lem)

main('.')
