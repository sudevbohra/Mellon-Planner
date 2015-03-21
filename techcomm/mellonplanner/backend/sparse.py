'''
Created on Oct 23, 2014

@author: Bill
'''

import re

clsinfos = []

f = open('soc_s14.csv', 'r')
clsinfo = None
for line in f:
    mm = re.findall(r'".*?"', line)
    for subs in mm:
        line = line.replace(subs, subs.replace(',',';')[1:-1])
    line = line.strip()
    #if line[:2] == '21':
    lsplit = line.split(',')
    cId, cName, lineInfo = lsplit[0],lsplit[1],lsplit[2:]
    if len(cId)>0:
        if clsinfo:
            clsinfos.append(clsinfo)
        clsinfo = [lineInfo]
    else:
        if clsinfo:
            clsinfo.append(lineInfo)
        else:
            clsinfo = [lineInfo]

print('\n'.join('%s'%c for c in clsinfos))

f.close()
#lines = [line for line in f if 'Pittsburgh' in line]