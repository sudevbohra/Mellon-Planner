'''
Created on Feb 16, 2015

@author: Bill
'''

import urllib2
import re

#re.DOTALL = True
#print(re.DOTALL)

def flatten(T):
    return [x for L in T for x in L]

def getPrereqs(coursenum, sem):
    URL = "https://enr-apps.as.cmu.edu/open/SOC/SOCServlet/courseDetails?COURSE=%s&SEMESTER=%s" % (coursenum, sem)

    ass = None
    try:
        ass = urllib2.urlopen(URL)
    except:
        return []
    fstr = ''.join(line.strip() for line in ass)
    #print(fstr)
    #print('-'*100)
    mo = re.match('.*<dl>.*?Prerequisites(.*?)</dl>.*', fstr)
    mn = None
    if mo:
        mn = re.findall('(\d+)', mo.group(1))
    ass.close()
    return [] if not mn else map(int, mn)

def getAllPrereqs(coursenum):
    l1 = getPrereqs(coursenum, 'F14')
    if len(l1)>0:
        return l1
    return getPrereqs(coursenum, 'S15')

def prereqChain(start):
    ps15 = lambda cn: getAllPrereqs(str(cn))

    G = {}
    X = set()
    F = set(start)
    while len(F) > 0:
        #print(F)
        X = X.union(F)
        for v in F:
            w = ps15(v)
            #print("(%s, %s)" % (v, w))
            #for t in w:
            #    print('%s -> %s,' % (v,t))
            G[v] = w
            F = F.union(set(w))
        F = F - X

    return G
    #print('-'*50)
    #print(X)

def topSort(G):
    visited = {k:False for k in G}
    #result = []
    def dfs(v):
        visited[v] = True
        for w in G[v]:
            if not (visited[w]):
                dfs(w)
        print(v)
    for k in G:
        dfs(k)



if __name__ == '__main__':
    dml_courses = [21441, 21355, 21341, 21301, 21300, 21228, 21484]
    cs_courses = [15251, 15210, 15122, 15317, 15150, 15151, 15213, 15451,
                  15221, 15354, 15355, 15453, 15455, 15456, 15312,
                  15410, 15411, 15418, 15440, 15441]
    phi_courses = [80310, 80311, 80405, 80411, 80413]

    #print('{')
    #gr = prereqChain(dml_courses + cs_courses)
    #print('}')
    #print("@"*10)
    #topSort(gr)

    print(getAllPrereqs('80311'))





