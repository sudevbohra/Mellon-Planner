'''
Created on Oct 23, 2014

@author: Bill
'''

from Tkinter import *
import random
from graphUtil import *
from sparse import getFullSchedule

def randomCVal():
    return int((255+ random.random()*256)/2)


def randomColor():
    r = randomCVal()
    g = randomCVal()
    b = randomCVal()
    return '#' + hex(r)[2:].zfill(2) + hex(g)[2:].zfill(2) + hex(b)[2:].zfill(2)


def intersects(t1,t2):
    for k in t1:
        if k in t2:
            (x1,y1),(x2,y2) = t1[k], t2[k]
            if x1 < y2 and y1 > x2:
                return True
    return False

def flattenClasses(clss):
    print(clss[0].tsplit())
    return [(fullId, t, cl) for cl in clss for (fullId,t) in cl.tsplit().items()]

def minStartTime(t):
    return min(v[0] for (_,v) in t.items())


#===============================================================================
# cls0 = Cls('15213', units=12)
# lec1 = Lec('TR', 13.50, 15)
# lec1.recs = {'A':Rec('M', 10.5, 11.5), 'B':Rec('M', 10.5, 11.5), 'C':Rec('M', 11.5, 12.5), 'D':Rec('M', 12.5, 13.5)}
# lec2 = Lec('TR', 18.5, 20)
# lec2.recs = {'I':Rec('M', 10.5, 11.5), 'J':Rec('M', 11.5, 12.5), 'K':Rec('M', 12.5, 13.5), 'L':Rec('M', 13.5, 14.5)}
# cls0.lecs = {'1': lec1, '2':lec2}
#
# clss_BILL = [cls0]
#===============================================================================


#ACTIVE_CLASS_LIST = clss_BILL
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


if __name__ == '__main__':
    fullSched = getFullSchedule(0)
    ACTIVE_CLASS_LIST = [fullSched['15213'],
                         fullSched['21300'],
                         fullSched['21441'],
                         fullSched['21355']]


    scheds,units = getScheds(ACTIVE_CLASS_LIST)

    print(len(scheds))
    print(scheds[0])

    classes = ACTIVE_CLASS_LIST

    ###############################################################################
    COLORS = [randomColor() for _ in range(100)]

    WIDTH = 1000
    HEIGHT = 800

    START_HR = 9
    NUM_HRS = 12

    RECT_PAD = 3

    linedx = WIDTH/7
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

        for i in range(1,7):
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
