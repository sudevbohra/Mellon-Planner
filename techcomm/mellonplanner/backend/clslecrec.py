'''
Created on Mar 22, 2015

@author: Bill
'''

dDict = {'U': -1, 'M':0, 'T':1, 'W':2, 'R':3, 'F':4, 'S': 5}

class Rec:
    def __init__(self, rDays, rTimeStart, rTimeEnd):
        self.rDays = [dDict[c] for c in rDays]
        self.timeInt = (rTimeStart, rTimeEnd)

    def tsplit(self):
        return {d: self.timeInt for d in self.rDays}

class Lec:
    def __init__(self, lDays, lTimeStart, lTimeEnd):
        self.lDays = [dDict[c] for c in lDays]
        self.timeInt = (lTimeStart, lTimeEnd)
        self.recs = {}

    def tsplit(self):
        if len(self.recs) == 0:
            return {'' : {d: self.timeInt for d in self.lDays}}
        else:
            options = {}
            base = {d: self.timeInt for d in self.lDays}
            for (rn, rec) in self.recs.items():
                b2 = base.copy()
                rec_tmap = rec.tsplit()
                b2.update(rec_tmap) #IMPORTANT ASSUMPTION: rec/lec never on same day; TODO: change
                options['.%s' % rn.replace(' ', '_')] = b2
            return options

class Cls:
    def __init__(self, cId, units=9):
        self.cId = cId
        self.lecs = {}

        self.units = units

    def tsplit(self):
        return {'%s.%s%s' % (self.cId, ln.replace(' ', '_'), rns) : cal for (ln, lec) in self.lecs.items() for (rns, cal) in lec.tsplit().items()}
