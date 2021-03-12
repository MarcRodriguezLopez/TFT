import pandas as pd
import re
import csv

teams_dict = {}
fouls_dict = {}
matchs_dict = {}

def getDict(teams, types, matchs):
    df = pd.read_csv(teams)
    for i in range(len(df)):
        team = df["Team"][i]
        id = df["Id"][i]
        teams_dict[team] = format(id, '02d')

    df = pd.read_csv(types)
    for i in range(len(df)):
        action = df["Action"][i]
        id = df["Id"][i]
        type = df["Type"][i]
        if "Foul" in type:
            fouls_dict[id] = action

    df = pd.read_csv(matchs)
    for i in range(len(df)):
        date = str(df["Year"][i]) + format(df["Month"][i], '02d') + format(df["Day"][i], '02d')
        vis = df["Away"][i]
        loc = df["Home"][i]
        res = str(date) + format(vis, '02d') + format(loc, '02d')
        matchs_dict[res] = df["Id"][i]


def parseCode(code):
    date = code[:-6]
    vis = code[-6:-3]
    loc = code[-3:]
    return matchs_dict[date + str(teams_dict[vis]) + str(teams_dict[loc])]


def checkFoul(fact):
    for i in range(len(fouls_dict)):
        if fouls_dict[i + 1] in fact:
            return i + 1
    return 0

def getTeam(fact):
    fact = fact.split(']')
    fact = fact[0].strip()
    if len(fact) > 4:
        if 'COACH' in fact:
            fact = fact.split(' COACH')
        elif 'ERROR' in fact:
            fact = fact.split(' ERROR')
        fact = fact[0]
    if len(fact) > 4:
        fact = fact[2:5]
    else:
        fact = fact[1:4]
    return teams_dict[fact]


def fillFile(code, time, fact, writerFouls):
    if ("Foul:" in fact) or ("Foul :" in fact):
        writerFouls.writerow([code, time, getTeam(fact), checkFoul(fact)])



def main(inputDoc, outputDoc, teams, types, matchs):
    with open(inputDoc) as dat_file, open(outputDoc, 'w', newline='') as FoulsWrite:
        writerFouls = csv.writer(FoulsWrite)
        writerFouls.writerow(['Code', 'Time', 'Team', 'FoulType'])

        getDict(teams, types, matchs)

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
            fillFile(parseCode(code), time.strip(), fact, writerFouls)