#!/usr/bin/env python
import os
import urllib
import re
from os import listdir
from os.path import isfile, join

class TakenClass:
    def __init__(self, num, data, dept="CS", title="",
                 preadmit=False, grade="", term="", year="", transfer=False):        
        path = re.match("^([A-Za-z]+) ([0-9]{3})(?: (.+?))?$", str(num))
        if (path):
            self.dept = path.group(1)
            self.num = path.group(2)
            self.title = path.group(3)
            key = str(num)
        else:
            self.num = num
            self.dept = dept
            self.title = None
            key = self.dept + " " + str(num)
        
        if (self.num == 510):
            if (self.title == None):
                self.title = title
            key += " " + self.title

        if (title == "" and self.title== None):
            self.title = data[key]['title']
        elif title != "":
            self.title = title


        self.key = key
        self.title = re.sub("^[A-Za-z]+ [0-9]{3}\s*", "", self.title)
        self.preadmit = preadmit
        self.transfer = transfer
        self.credits = int(data[key]['credits'])
        self.grade = grade
        self.term = term
        self.year = year

    def lines (self):
        s = ""
        s += self.dept + " "
        s += str(self.num) + " "
        s += self.title + " "
        s += "(" + str(self.credits) + " credits) "

        if (self.year):
            s += self.term + "/" + str(self.year) + "/PDX"
        
        return s

    def report (self):
        s = ""
        if (self.preadmit):
            s += "P";
        s += " & "
        if (self.transfer):
            s += "T";
        s += " & "
        s += self.dept + " & "
        s += str(self.num) + " & "
        s += self.title + " & "
        s += str(self.credits) + " & "
        s += self.grade + " & "

        if (self.year):
            s += self.term + "/" + str(self.year) + "/PDX"
        
        s += ' \\\\ \\hline'
        return s

choices={
    'base':{'req':[581,558,533], 'c':0, 'opt':[], '510':[]},
    'db':{'req':[586,587], 'c':1, 'opt':[588],
          '510':['Information Integration', 'Data Streams']},
    'ai':{'req':[541,545], 'c':1, 'opt':[542,543,546], '510':[]},
    'lang':{'req':[558], 'c':2, 'opt':[515,520,553,557,568,577,578],
            '510':['Functional Logic Programming']},
    'sec':{'req':[591,585], 'c':1, 'opt':[592,576,676,596,696],
           '510':['Malicious Code and Forensics', 'Intro. to Computer Forensics']},
    'eng':{'req':[554], 'c':2, 'opt':[552,553,555,556,559],
           '510':['Software Quality Analysis', 'Modeling and Analysis of Software Systems',
                  'Software Architecture and Domain Analysis', 'Software Design Techniques',
                  'Adv. Topics in Software Engineering', 'Advanced Open Source Software Engineering',
                  'Software Development and Testing']},
    'sys':{'req':[533,594], 'c':1, 'opt':[595,596,572,575,597], 
           '510':['Intro. to Multimedia Networking', 'Adv. Multimedia Networking']},
    'theory':{'req':[581,584], 'c':1, 'opt':[582,585], 
              '510':['Scheduling, Planning and Search']}
}

mypath = "corpus/"
files = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]

data = {}

for p in files:
    t = open(mypath + p, "rU").read()
    t = re.sub("&amp;amp;", "&amp;", t)
    t = re.sub("&amp;", "and", t)
    t = re.sub("CS 510:? Advanced", "CS 510 Top: Advanced", t)
    t = re.sub("410/510", "510 Top:", t)
    t = re.sub("Advanced", "Adv.", t)
    t = re.sub("Introduction", "Intro.", t)
    pre_reqs = list(set(re.findall(
                "(?:CS|MATH|MTH|STATS) [0-9]+(?:(?: Top)?:(?:[a-zA-Z\. \-,:/]|&amp;)+)?",
                t, re.IGNORECASE)))
    name_match = re.search('id="page-title">(.+?)</h1>', t)
    cs_match = re.search('CS [0-9]+', name_match.group(1))
    try:
        pre_reqs.remove(name_match.group(1))
    except:
        pass

    try:
        pre_reqs.remove(cs_match.group(0))
    except:
        pass
    
    if (re.search("510|410", cs_match.group(0))):
        name = name_match.group(1)
    else:
        name = cs_match.group(0)

    c_hours = re.search('Credit Hours:(?:</p>)?\s*</td>\s*<td(?: valign="top")?>\s*(?:<p>)?([0-9]+|TBD|)',
                        t, re.MULTILINE | re.IGNORECASE)
    c_hours_num = c_hours.group(1);
    if (name_match.group(1) == "CS 510 Top: Intro. to Visual Computing"):
        c_hours_num = "3"

    if (name_match.group(1) == "CS 510 Top: Adv. Cryptography"):
        pre_reqs = ["CS 585" if x == "CS 485" else x for x in pre_reqs]

    data[name] = {'title':name_match.group(1), 'reqs':pre_reqs, 'credits':c_hours_num}

def get_reqs(taken, data, cname):
    reqs = []
    if (cname in taken):
        pass
    else:
        if (not data.has_key(cname)):
            return [cname + ' (Unknown Dependencies)']

        reqs = [cname]
        for p in data[cname]['reqs']:
            reqs += get_reqs(taken, data, p)

    return reqs

#APLI no longer exists (manually adding it)
data["CS 510 Top: Adv. Programming Language Implementation"] = \
   {'title':'Adv. Programming Language Implementation', 'reqs':[], 'credits':3}

done = [
    #TakenClass(457, data, term="Winter", year=2012, grade="A", preadmit=True),
        TakenClass(558, data, term="Fall", year=2012, grade="A"),
        TakenClass(533, data, term="Winter", year=2013, grade="A"),
        TakenClass(581, data, term="Spring", year=2013, grade="A"),
        TakenClass(547, data, term="Fall", year=2013, grade="A"),
        TakenClass(553, data, term="Winter", year=2014, grade="A"),
        TakenClass(510, data, title="Top: Adv. Programming Language Implementation", term="Spring", year=2014, grade="A"),
        TakenClass(591, data, term="Fall", year=2014),
        ]

need=['CS 584', #Algorithms analysis, Requested by gord (probably tough as hell)
      'CS 580', #Randomized Algorithms and Probabilistic Analysis #Recommended by MPJ
      'CS 585', #Cryptography, also requested by gord.
      'CS 591', #Intro to Computer Security
      'CS 515', #Parallel Programming (NOTE: FORTRAN?!)
      'CS 550', # Parallel Algorithms'
      'CS 510 Top: Adv. Programming Language Implementation', #Replaces Modern Language Processors (this is probably what gordon wanted
      'CS 510 Top: Adv. Programming',
      'CS 572', #Operating System Internals, Gord Swap #'CS 510 Top: Adv. Cryptography',
      'CS 510 Top: Intro. to Visual Computing'
      ]

#mth 261 is intro to linear algebra
#stats 451 is applied statistics for engineers
taken_pre_reqs = ['CS 333', #Basic OSs, did 533, should be good
       'CS 202', #Computer Systems Programming, should be good
       'CS 106', #Computing Fundamentals
       'CS 161', #Intro to Programming, should be good
       'CS 162', #Intro to Computer Science, should be good
       'CS 300', #Elements of Software Engineering
       'CS 310', 'CS 340', # OOP Dependences that no longer exist?
       'CS 350', 'CS 250', 'CS 251', 'CS 321', 'CS 322', 'CS 311',
       'MTH 261', #linear algebra
]

taken = list(set([d.key for d in done] + need + taken_pre_reqs))

def print_courses(prefix, key):
    for r in v[key]:
        name = prefix + str(r)
        fullname = name
        if name in data:
           fullname = data[name]['title']
 
        if not name in taken:
            print fullname + ': ' + str(get_reqs(taken, data, name))
        else:
            print fullname + " TAKEN"

for t,v  in choices.items():
    reqs = []
    opts = []
    print ("=" * 5) + t + ("=" * 5)
    print " *** Courses Needed For " + t
    print_courses('CS ', 'req')
    print " *** Optional Courses (need " + str(v['c']) + "):"
    print_courses('CS ', 'opt')
    print_courses('CS 510 Top: ', '510')
    

creds_done = 0                     
for m in done:
    creds_done += m.credits

need_reqs = []
for n in need:
    need_reqs += get_reqs([d.key for d in done] + taken_pre_reqs, data, n)

creds_need = 0      
all_needed = list(set(need + need_reqs).difference(set([d.key for d in done])))
for n in all_needed:
    creds_need += int(data[n]['credits'])

print "========================================"
print "Credits Completed : " + str(creds_done)
print "Proposed: " + str(creds_need)
print "Need 45 Total:" + str(creds_done + creds_need)

#for a in all_needed:
#    print data[a]['title'] + " " + data[a]['credits']

proposed = list(set(all_needed + [d.key for d in done]))
for t,v  in choices.items():
    meet = True
    for x in v['req']:
        if (not 'CS ' + str(x) in proposed):
            meet = False

    count = 0
    for x in v['opt']:
        if ('CS ' + str(x) in proposed):
            count += 1
    
    for x in v['510']:
        if ('CS 510 Top:' + str(x) in proposed):
            count += 1

    if (count >= v['c'] and meet):
        print "  Proposed Plan meets requirements for " + t
    elif (not meet):
        print "  Missing requireds for " + t
    else:
        print "  Missing Optionals for " + t + " " + str(count) + "/" + str(v['c'])

print "========================================"

done += [TakenClass(a, data) for a in all_needed]

latex = False
if latex:
    print """
\\include{tabular}


\\documentclass[11pt]{article}
\\usepackage[top=2in, bottom=1.5in, left=1in, right=1in]{geometry}
\\date{}
\\begin{document}

Boss requests:
CS584
CS585
CS577
CS572

\\begin{tabular}{| c | c | c | c | p{5cm} | c | c | r |}
\\hline
P & T & DEPT. & NO. &TITLE &CR &GRADE &TRM \\\\
\\hline"""
else:
    print "P T DEPT NO. TITLE CR GRADE TRM"

for t in done:
    if latex:
        print t.report()
    else:
        print t.lines()

if latex:
    print """
\\end{tabular}
\\end{document}
"""
