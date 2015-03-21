'''
Created on Oct 23, 2014

@author: Bill
'''

from Tkinter import *
import random
from graphUtil import *

def randomCVal():
    return int((255+ random.random()*256)/2)


def randomColor():
    r = randomCVal()
    g = randomCVal()
    b = randomCVal()
    return '#' + hex(r)[2:].zfill(2) + hex(g)[2:].zfill(2) + hex(b)[2:].zfill(2)



dDict = {'M':0, 'T':1, 'W':2, 'R':3, 'F':4}


class Cls:
    def __init__(self, cId, lDays, lTimeStart, lTimeEnd, recDay=None, recTimes=[], units=9):
        self.cId = cId
        self.lDays = list(map(lambda c: dDict[c], lDays))
        self.lTimeStart = lTimeStart
        self.lTimeEnd = lTimeEnd
        self.recDay = dDict[recDay] if recDay else None
        self.recTimes = recTimes
        self.units = units
        self.tmap = self.tsplit()

    def tsplit(self):
        d = {i:(self.lTimeStart, self.lTimeEnd) for i in self.lDays}
        if self.recDay:
            ds = []
            for (ts,te) in self.recTimes:
                d2 = d.copy()
                d2[self.recDay] = (ts,te)
                ds.append(d2)
            return ds
        else:
            return [d]


def intersects(t1,t2):
    for k in t1:
        if k in t2:
            (x1,y1),(x2,y2) = t1[k], t2[k]
            if x1 < y2 and y1 > x2:
                return True
    return False

def flattenClasses(clss):
    return [('%s_%s' % (cl.cId,i), t, cl) for cl in clss for (i,t) in enumerate(cl.tmap)]

def minStartTime(t):
    return min(v[0] for (_,v) in t.items())




clss_BILL = [
    Cls('15214', 'TR', 15, 16.5, 'W', [(9.5,10.5),(10.5,11.5),(11.5,12.5),(12.5,13.5),(13.5,14.5)], units=12),
    Cls('15221', 'TR', 9, 10.5, 'F', [(9.5,10.5),(10.5,11.5),(11.5,12.5)]),
    Cls('15312', 'TR', 13.5, 15, 'W', [(11.5,12.5),(12.5,13.5)], units=12),
    Cls('15322', 'TR', 10.5, 12),
    Cls('15410', 'MWF', 10.5,11.5 , units=12),
    Cls('15418', 'MW', 13.5,15, units=12),
    Cls('15440', 'TR', 10.5,12, units=12),
    Cls('15453', 'TR', 12,13.5),
    Cls('15451', 'MW', 10.5, 12, 'T', [(9.5,10.5),(10.5,11.5),(12.5,13.5)], units=12),

    Cls('21201', 'R', 13.5,14.5),
    Cls('21268', 'MWF', 13.5,14.5, 'T', [(13.5,14.5),(15.5,16.5)], units=10),
    Cls('21269', 'MWF', 13.5,14.5, 'T', [(13.5,14.5)]),
    Cls('21301', 'MWF', 9.5,10.5),
    Cls('21329', 'MWF', 13.5,14.5),
    Cls('21366', 'MWF', 12.5, 13.5),
    Cls('21374', 'MWF', 12.5,13.5),
    Cls('21400', 'MWF', 14.5,15.5),
    Cls('21484', 'MWF', 11.5,12.5),

    Cls('11411', 'TR', 15.0, 16.5, units=12),
    Cls('80311', 'MW', 10.5,11.5, 'F', [(9.5,10.5),(10.5,11.5)]),
    Cls('80413', 'MW', 13.5,15),
    Cls('RRR', 'TR', 13.5, 15)
    ]

clss_TERRI = [
    Cls('Cog Psych', 'MWF', 10.5, 11.5),
    Cls('Research Methods 0', 'TR', 10.5, 12),
    Cls('Research Methods 1', 'TR', 13.5, 15),
    Cls('Personality', 'TR', 15,16.5),
    Cls('Physiology', 'MWF', 12.5, 13.5),
    Cls('Chem Lab I', 'TR', 10.5, 11.5),
    Cls('ChemLabRec0', 'MW', 13.5, 16.5),
    Cls('ChemLabRec1', 'TR', 13.5, 16.5),
    Cls('Social Factors', 'MW', 15, 16.5),
    Cls('Practicum in CD', 'W', 10.5, 12),
    Cls('Internship', 'M', 16.5, 17.5),
    Cls('Crosscultural Psych', 'MW', 10.5, 12),
    ]


ACTIVE_CLASS_LIST = clss_BILL
#print(units)

def getScheds(clss):
    tsg = flattenClasses(clss)

    N = len(tsg)
    intersectionMatrix = [[1 if i==j else int(tsg[i][2].cId == tsg[j][2].cId or intersects(tsg[i][1],tsg[j][1])) for i in range(N)] for j in range(N)]

    maxIndepSets = sorted(independentSet(intersectionMatrix), key=len)

    scheds = [[tsg[i] for i in s] for s in maxIndepSets]
    units = [sum(t[2].units for t in s) for s in scheds]
    scheds = sorted(zip(units,scheds),key=lambda t: t[0])
    scheds = [t[1] for t in scheds]
    return scheds,units


scheds,units = getScheds(ACTIVE_CLASS_LIST)

classes = ACTIVE_CLASS_LIST

###############################################################################
COLORS = [randomColor() for _ in range(100)]

WIDTH = 1000
HEIGHT = 800

START_HR = 9
NUM_HRS = 10

RECT_PAD = 3

linedx = WIDTH/6
linedy = HEIGHT/NUM_HRS

root = Tk()
root.resizable(0,0)

ACTIVE_CANVAS = None
def drawSchedule(sched):
    global ACTIVE_CANVAS
    if ACTIVE_CANVAS:
        ACTIVE_CANVAS.pack_forget()
    c = Canvas(root, background='floral white', width=WIDTH, height=HEIGHT)
    ACTIVE_CANVAS = c

    for i in range(1,6):
        x = i*linedx
        c.create_line(x,0,x,HEIGHT)

    for i in range(NUM_HRS):
        hr = START_HR + i
        y = i*linedy
        c.create_line(0,y,WIDTH,y)
        c.create_line(0,y+linedy/2,WIDTH,y+linedy/2, dash=(100,10))
        c.create_text(5,y+5,anchor=NW,text=str((hr-1)%12 + 1))


    for (idx,(cIdr, td, cl)) in enumerate(sched):
        col = COLORS[idx]
        for (i,(v0,v1)) in td.items():
            x0 = (i+1)*linedx+RECT_PAD
            x1 = (i+2)*linedx-RECT_PAD
            y0 = (v0-START_HR)*linedy+RECT_PAD
            y1 = (v1-START_HR)*linedy-RECT_PAD
            c.create_rectangle(x0,y0,x1,y1, fill=col)
            c.create_text((x0+x1)/2,(y0+y1)/2,text=str(cIdr))

    c.pack()


activeClassVars = [IntVar() for _ in ACTIVE_CLASS_LIST]
forceClassVars = [IntVar() for _ in ACTIVE_CLASS_LIST]
def refreshLists():
    global classes, scheds, units

    classes = [ACTIVE_CLASS_LIST[i] for i in range(len(ACTIVE_CLASS_LIST)) if activeClassVars[i].get()]

    scheds, units = getScheds(classes)

    forceCIDs = [ACTIVE_CLASS_LIST[i].cId for i in range(len(ACTIVE_CLASS_LIST)) if forceClassVars[i].get()]
    def schedMatches(s):
        sat = {fId:0 for fId in forceCIDs}
        for (_,_,cl) in s:
            if cl.cId in sat:
                sat[cl.cId] = 1
        sats = all(sat.values())
        return sats

    validIndices = [i for i in range(len(scheds)) if schedMatches(scheds[i])]
    scheds = [scheds[i] for i in validIndices]
    units = [units[i] for i in validIndices]

    loadList()

lFrame = Frame(root)

includeCBFrame = Frame(lFrame)
Label(includeCBFrame, text="Include:").pack(side=TOP,anchor=W)

for i in range(len(classes)):
    cl = classes[i]
    cb0 = Checkbutton(includeCBFrame, text=cl.cId, var=activeClassVars[i])
    cb0.select()
    cb0.pack(side=TOP, anchor=W)
includeCBFrame.pack(side=LEFT, fill=Y)

forceCBFrame = Frame(lFrame)
Label(forceCBFrame, text="Force:").pack(side=TOP,anchor=W)

for i in range(len(classes)):
    cl = classes[i]
    cb0 = Checkbutton(forceCBFrame, text=cl.cId, var=forceClassVars[i])
    cb0.pack(side=TOP, anchor=W)
forceCBFrame.pack(side=LEFT, fill=Y)

Button(lFrame, text="Get", command=refreshLists).pack(side=BOTTOM)

lFrame.pack(side=LEFT, fill=BOTH, expand=TRUE)

scrollbar = Scrollbar(root)

schedLb = Listbox(root, width=30, selectmode=SINGLE)

def loadList():
    schedLb.delete(0,END)

    for i in range(len(scheds)):
        schedLb.insert(END,'%s (%s)' % (i,units[i]))

loadList()

schedLb.selection_set(END)

def switchSched(event):
    i = int(schedLb.curselection()[0])
    drawSchedule(scheds[i])


schedLb.bind("<<ListboxSelect>>", switchSched)
schedLb.pack(side=LEFT,anchor=W,fill=Y,expand=True)
scrollbar.pack(side=LEFT, fill=Y)

schedLb.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=schedLb.yview)

drawSchedule(scheds[-1])
root.mainloop()
