import csv
import re

turnoverlist = []
pointslist = []
restlist = []
foulslist = []

def fillTurnoverList(fact):
    if "Turnover: " in fact and " (" in fact and "] " in fact:
        thisfact = fact.split('] ')
        thisfact = thisfact[1].split('Turnover: ')
        thisfact = thisfact[1].split(' (')
        turnoverlist.insert(len(turnoverlist), thisfact[0])


def fillPointsList(fact, list):
    if ": Made" in fact and "] " in fact:
        thisfact = fact.split('] ')
        thisfact = thisfact[1].split(': Made')
        thisfact = thisfact[0]
    elif ": Missed" in fact and "] " in fact:
        thisfact = fact.split('] ')
        thisfact = thisfact[1].split(': Missed')
        thisfact = thisfact[0]
    else:
        thisfact = 'Pietrus Jump Shot'

    for player in list:
        if player in thisfact:
            a = player.split()
            b = thisfact.split()
            lol = 0
            for x in range(len(a)):
                if a[x] in b:
                    lol = lol + 1
            if lol == len(a):
                thisfact = thisfact.split(player)
                pointslist.insert(len(pointslist), thisfact[1].strip())
    pointslist.insert(len(pointslist), 'Free Throw')


def fillRestList(fact):
    if "Timeout: " in fact:
        thisfact = fact.split("Timeout: ")
        restlist.insert(len(restlist), "Timeout: " + thisfact[1].strip())
    elif "Violation: " in fact:
        thisfact = fact.split("Violation: ")
        restlist.insert(len(restlist), "Violation: " + thisfact[1].strip())
    elif "Instant Replay: " in fact:
        thisfact = fact.split("Instant Replay: ")
        restlist.insert(len(restlist), "Instant Replay: " + thisfact[1].strip())
    elif "Ejection: " in fact:
        thisfact = fact.split("Ejection: ")
        restlist.insert(len(restlist), "Ejection: " + thisfact[1].strip())


def fillFoulsList(fact):
    if "Foul: " in fact and " (" in fact and "] " in fact:
        thisfact = fact.split('] ')
        thisfact = thisfact[1].split(' (')
        thisfact = thisfact[0].split('Foul: ')
        foulslist.insert(len(foulslist), thisfact[1])


def putNumbers(turnoverlist, pointslist, restlist, foulslist, csv_file):
    turnoverlist = list(dict.fromkeys(turnoverlist))
    turnoverlist.sort(reverse=True, key=len)
    pointslist = list(dict.fromkeys(pointslist))
    pointslist.sort(reverse=True, key=len)
    restlist = list(dict.fromkeys(restlist))
    restlist.sort(reverse=True, key=len)
    foulslist = list(dict.fromkeys(foulslist))
    foulslist.sort(reverse=True, key=len)
    i = 1
    writer = csv.writer(csv_file)
    writer.writerow(["Action", "Id", "Type"])
    for n in turnoverlist:
        writer.writerow([n, i, "Turnover"])
        i = i + 1
    i = 1
    for n in pointslist:
        writer.writerow([n, i, "Shot"])
        i = i + 1
    i = 1
    for n in foulslist:
        writer.writerow([n, i, "Foul"])
        i = i + 1
    i = 1
    for n in restlist:
        writer.writerow([n, i, "Rest"])
        i = i + 1


def main(inputDoc, outputDoc):
    with open(inputDoc) as dat_file, open(outputDoc, 'w', newline='') as csv_file:
        a = 0
        playerslist = []
        for line in dat_file:
            a = a + 1
            """
            code = res[:15]
            id = res[15:28]
            time = res[28:43]
            fact = res[43:]
            """
            res = ""
            for x in range(len(line)):
                res += line[x]
            x = re.findall("[0-9]{2}\:[0-9]{2}\:[0-9]{2}\s+.+", res)
            fact = x[0][8:].strip()

            if "Substitution" in fact and a < 2000:
                thisfact = fact.split('] ')
                thisfact = thisfact[1].split(' Substitution replaced by ')
                playerslist.insert(len(playerslist), thisfact[0].strip())
                playerslist.insert(len(playerslist), thisfact[1].strip())
            if a == 2000:
                playerslist = list(dict.fromkeys(playerslist))

            if "Foul" in fact:
                fillFoulsList(fact)
            elif ("Made" in fact and a > 2000) or ("Missed" in fact and a > 2000):
                fillPointsList(fact, playerslist)
            elif "Turnover" in fact:
                fillTurnoverList(fact)
            else:
                fillRestList(fact)
        putNumbers(turnoverlist, pointslist, restlist, foulslist, csv_file)
