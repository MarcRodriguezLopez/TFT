import pandas as pd
import re
import csv
import os

previousTime = 0
aux = 0

teams_dict = {}
matchs_dict = {}

def getDict(teams, matchs):
    df = pd.read_csv(teams)
    for i in range(len(df)):
        team = df["Team"][i]
        id = df["Id"][i]
        teams_dict[team] = format(id, '02d')

    df = pd.read_csv(matchs)
    for i in range(len(df)):
        date = str(df["Year"][i]) + format(df["Month"][i], '02d') + format(df["Day"][i], '02d')
        vis = df["Away"][i]
        loc = df["Home"][i]
        res = str(date) + format(vis, '02d') + format(loc, '02d')
        matchs_dict[res] = df["Id"][i]


def parseCode(code):
    date = code[0:-6]
    vis = code[-6:-3]
    loc = code[-3:]
    return matchs_dict[date + str(teams_dict[vis]) + str(teams_dict[loc])]

def getTeam(fact):
    fact = fact.split('] ')
    fact = fact[0].strip()
    fact = fact[1:4]
    return teams_dict[fact]


def fillFile(code, time, fact, writerSubs):
    global previousTime, aux
    if "Substitution" in fact:
        if previousTime == time:
            aux = aux + 1
        else:
            aux = 1
        previousTime = time
        writerSubs.writerow([code, time, getTeam(fact), aux])


def main(inputDoc, outputDoc, teams, matchs):
    with open(inputDoc) as dat_file, open('SubstitutionsAuxO.csv', 'w', newline='') as SubsWrite, open(
            'SubstitutionsAuxO.csv', 'r') as SubsRead, open('SubstitutionsAux.csv', 'w', newline='') as SubsAuxWrite, open(
            'SubstitutionsAux.csv', 'r') as SubsAuxRead, open(outputDoc, 'w', newline='') as OutputFile:
        writerSubs = csv.writer(SubsWrite)
        writerSubs.writerow(['Code', 'Time', 'Team', 'Number'])

        getDict(teams, matchs)

        for line in dat_file:
            """
            code = res[:15]
            id = res[15:28]
            time = res[28:43]
            fact = res[43:]
            """
            res = ""
            for x in range(len(line)):
                res += line[x]
            x = re.findall("[0-9]{8}[A-Z]{6}", res)
            code = x[0]
            x = re.findall("\-?[0-9]{2}\:[0-9]{2}\:[0-9]{2}", res)
            time = x[0]
            x = re.findall("[0-9]{2}\:[0-9]{2}\:[0-9]{2}\s+.+", res)
            fact = x[0][8:].strip()
            fillFile(parseCode(code), time.strip(), fact, writerSubs)

        dat_file.close()
        SubsWrite.close()

        writerSubsAux = csv.writer(SubsAuxWrite)

        a = ''
        b = ''
        for row in reversed(list(csv.reader(SubsRead))):
            if row[0] != a or row[1] != b:
                writerSubsAux.writerow([row[0], row[1], row[2], row[3]])
            a = row[0]
            b = row[1]

        SubsRead.close()
        SubsAuxWrite.close()

        writerOutput = csv.writer(OutputFile)

        for row in reversed(list(csv.reader(SubsAuxRead))):
            writerOutput.writerow([row[0], row[1], row[2], row[3]])

        SubsAuxRead.close()
        OutputFile.close()

    os.remove('SubstitutionsAux.csv')
    os.remove('SubstitutionsAuxO.csv')