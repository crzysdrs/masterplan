#!/usr/bin/env python
import json
import argparse
import sys

def strClass(c, classlist):
    actual = findClass(c, classlist)
    return "%s %s: %s" % (actual['dept'], actual['num'], actual['title'])

def vMsg(args, msg):
    if args.verbose:
        print msg

def verifyTrack(args, plan, track, classlist):
    vMsg(args, "*********** Track: %s **************" % track['name'])
    error = False
    for r in track['req']:
        if not findClass(r, plan):
            error = True
            vMsg(args, "Missing required " + strClass(r, classlist))
        else:
            vMsg(args, "Have required " + strClass(r, classlist))

    if track['choose'] > 0:
        count = 0
        for c in track['optional']:
            if findClass(c, plan):
                count += 1
                vMsg(args, "Have optional " + strClass(c, classlist))

        if count < track['choose']:
            error = True
            vMsg(args, "Missing too many optionals!")
        else:
            vMsg(args, "Plan has required number of optionals")
        vMsg(args, "%d/%d optionals" % (count, track['choose']))

    if error:
        vMsg(args, "Plan does not meet requirements for " + track['name'])
    else:
        vMsg(args, "Plan meets requirements for " + track['name'])

    return not error

def findClass(find, classlist):
    for c in classlist:
        if find['dept'] != c['dept'] or find['num'] != c['num']:
            continue
        elif not 'title' in find:
            return c
        elif find['title'] == c['title']:
            return c

    return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Validate Master Plan')
    parser.add_argument('--school', default='pdx.json', help='json file describing school tracks')
    parser.add_argument('--verbose', '-v', help='verbose information about plans', action="count")
    parser.add_argument('--showplan', help='prints out plan', action='store_true', default=False)
    parser.add_argument('plan', help='json file with plan')
    args = parser.parse_args()

    school = json.load(open(args.school))
    plan = json.load(open(args.plan))
    
    error = False
    for c in plan:
        if not findClass(c, school['classes']):
            if 'title' in c:
                title = c['title']
            else:
                title = ''
            print "Unable to find class %s %s %s in class list." % (c['dept'], c['num'], title)
            error = True
    
    for t in school['tracks']:
        for r in t['req']:
            if not findClass(r, school['classes']):
                print "Can't find required class %s %s from track %s" % (r['dept'], r['num'], t['name'])
                error = True
        if t['choose'] > 0:
            for c in t['optional']:
               if not findClass(r, school['classes']):
                print "Can't find optional class %s %s from track %s" % (c['dept'], c['num'], c['name'])
                error = True 
    if error:
        sys.exit(1)

    match_tracks = []
    for t in school['tracks']:
        if verifyTrack(args, plan, t, school['classes']):
            match_tracks.append(t)

    print "***** Plan meets requirements for tracks: %s" % ", ".join(map(lambda t: t['name'], match_tracks))
    
    credits = 0
    for c in plan:
        found = findClass(c, school['classes'])
        credits += found['credits']

    if credits < school['required_credits']:
        print "Not enough credits!"

    print "Credits %d/%d" % (credits, school['required_credits'])

    if args.showplan:
        print "--------- Plan ----------"
        for c in plan:
            term = "<Term>"
            if 'term' in c:
                term = c['term']
            year = "<XXXX>"
            if 'year' in c:
                year = c['year']

            print "%s (%s %s)" % (strClass(c, school['classes']), term, year)
