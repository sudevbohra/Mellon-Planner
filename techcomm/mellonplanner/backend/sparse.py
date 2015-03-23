'''
Created on Mar 21, 2015

@author: Bill
'''

import urllib2
import re
from clslecrec import Cls, Lec, Rec

import time

BASE_URL = "https://enr-apps.as.cmu.edu/assets/SOC/"
URL_SUFFIXES = ['sched_layout_fall.htm',
                'sched_layout_spring.htm',
                'sched_layout_summer_1.htm',
                'sched_layout_summer_2.htm']

INDEX = {  'blank':0,
           'id':1,
           'name':2,
           'units':3,
           'lecsec':4,
           'days':5,
           'timestart':6,
           'timeend':7,
           'location':8,
           'instructors':9}

LINE_SPLIT_RE = r'<TR><TD.*?>|<TD.*?>|</TD><TD.*?>|</TD></TR>'
LEC_RE = r'Lec\w*\d*'


def parseTime(timeStr):
    #parse time format HH:MM(AM/PM)
    hr = int(timeStr[:-5])
    minute = round(float(timeStr[-4:-2])/60.0 * 2)/2.0
    ampm = timeStr[-2:]
    if ampm.lower() == 'pm' and hr != 12:
        hr += 12
    if ampm.lower() == 'am' and hr == 12:
        hr = 0
    return hr + minute

def parseSched(f):

    sched = {}
    activeCls = None
    activeLec = None
    lecStyle = False

    # f is an html file object
    i = 0
    for line in f:
        line = line.strip()
        line = line.replace('&nbsp;', '')

        tokens = re.split(LINE_SPLIT_RE, line)
        #print(tokens)

        if len(tokens) == 12:
            cid = tokens[INDEX['id']]
            name = tokens[INDEX['name']]
            units = tokens[INDEX['units']]
            lecsec = tokens[INDEX['lecsec']]
            days = tokens[INDEX['days']]
            timestart = tokens[INDEX['timestart']]
            timeend = tokens[INDEX['timeend']]
            location = tokens[INDEX['location']]
            instructors = tokens[INDEX['instructors']]



            if cid:
                # new class
                if activeCls:
                    sched[activeCls.cId] = activeCls
                try:
                    _ = int(cid)
                    activeCls = Cls(cid, int(float(units)) if units else 0)
                except:
                    pass



            if not timestart or not timeend:
                continue
            timestart = parseTime(timestart)
            timeend = parseTime(timeend)

            if cid:
                activeLec = Lec(days, timestart, timeend)
                activeCls.lecs = {lecsec:activeLec}
                if re.match(LEC_RE, lecsec):
                    lecStyle = True
            elif lecsec and re.match(LEC_RE, lecsec):
                #new lecture in style "Lec..."
                lecStyle = True
                activeLec = Lec(days, timestart, timeend)
                activeCls.lecs[lecsec] = activeLec
            elif lecsec and not lecStyle:
                #new lecture in other style
                activeLec = Lec(days, timestart, timeend)
                activeCls.lecs[lecsec] = activeLec
            elif lecsec:
                #recitation
                newRec = Rec(days, timestart, timeend)
                activeLec.recs[lecsec] = newRec


        i += 1


    return sched


def getFullSchedule(semIndex):
    url = BASE_URL + URL_SUFFIXES[semIndex]

    conn = None
    try:
        conn = urllib2.urlopen(url)
    except Exception as e:
        print("Unable to connect to %s\n%s" % (url, e))
        return None

    result = parseSched(conn)

    conn.close()

    return result

if __name__ == '__main__':
    #print(parseTime('12:50AM'))
    t0 = time.clock()
    msched = getFullSchedule(0)
    print('Success .. %f' % (time.clock() - t0))
    print(msched['21355'].tsplit())
