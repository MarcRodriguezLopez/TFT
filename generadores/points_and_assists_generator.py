import pandas as pd
import re
import csv

auxPoints = 0
value = 0
teams_dict = {}
shot_dict = {}
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
        if "Shot" in type:
            shot_dict[id] = action

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


def actualPoints(fact):
    fact = fact.strip()
    fact = fact.split('] ')
    fact = fact[0].split(' ')
    fact = fact[1].split('-')
    return int(fact[0]) + int(fact[1])


def checkShot(fact):
    for i in range(len(shot_dict)):
        if shot_dict[i + 1] in fact:
            return i + 1
    return 0

def getTeam(fact):
    fact = fact.split('] ')
    fact = fact[0].strip()
    fact = fact[1:4]
    return teams_dict[fact]


def fillPointsFile(code, time, fact, writer):
    global auxPoints, value
    if " PTS)" in fact:
        actual = actualPoints(fact)
        value = actual - auxPoints
        value = abs(value)
        if checkShot(fact) == 67:
            value = 1
        elif value > 3:
            value = actual
        auxPoints = actual
        writer.writerow([code, time, getTeam(fact), checkShot(fact), 1, value])
    elif "issed" in fact:
        writer.writerow([code, time, getTeam(fact), checkShot(fact), 0, 0])

def fillAssistsFile(code, time, fact, writer_assists):
    global value
    if 'Assist' in fact and ' AST)' in fact:
        writer_assists.writerow([code, time, getTeam(fact), value])

# def fillLolFile(code, time, id, fact, writer_lol):
#     if " PTS)" in fact:
#         a = code*1000 + int(id)
#         writer_lol.writerow([a, time, fact])
#     elif "issed" in fact:
#         a = code*1000 + int(id)
#         writer_lol.writerow([a, time, fact])

def main(inputDoc, outputPointsDoc, lol, outputAssistsDoc, teams, types, matchs):
    with open(inputDoc) as dat_file, open(outputPointsDoc, 'w', newline='') as csv_file, open(outputAssistsDoc, 'w', newline='') as csv_file_assists:
        writer = csv.writer(csv_file)
        writer_assists = csv.writer(csv_file_assists)
        # writer_lol = csv.writer(csv_file_lol)
        # writer_lol.writerow(['Id', 'Time', 'Action'])
        writer_assists.writerow(['Code', 'Time', 'Team', 'PointsGenerated'])
        writer.writerow(['Code', 'Time', 'Team', 'TypeShot', 'MissOrMade', 'Value'])

        getDict(teams, types, matchs)

        # for line in dat_file:
        #     """
        #     code = res[:15]
        #     id = res[15:28]
        #     time = res[28:43]
        #     fact = res[43:]
        #     """
        #     res = ""
        #     for x in range(len(line)):
        #         res += line[x]
        #     x = re.findall("[0-9]{8}[A-Z]{6}", res)
        #     code = x[0]
        #     x = re.findall("\s[0-9]{1,3}\s", res)
        #     id = x[0]
        #     x = re.findall("\-?[0-9]{2}\:[0-9]{2}\:[0-9]{2}", res)
        #     time = x[0]
        #     x = re.findall("[0-9]{2}\:[0-9]{2}\:[0-9]{2}\s+.+", res)
        #     fact = x[0][8:].strip()
            # fillLolFile(parseCode(code), time.strip(), id, fact, writer_lol)
            #fillPointsFile(parseCode(code), time.strip(), fact, writer)
            #fillAssistsFile(parseCode(code), time.strip(), fact, writer_assists)

        # df = pd.read_csv('lol.csv')
        # print(len(df))
        # df = df.sort_values(by=['Id'])
        # print(len(df))
        # df.to_csv('sorted.csv')

        df1 = pd.read_csv('sorted.csv')
        for i in range(len(df1)):
            time = df1["Time"][i]
            action = df1["Action"][i]
            code = df1["Id"][i]
            fillPointsFile(code // 1000, time, action, writer)
            fillAssistsFile(code // 1000, time, action, writer_assists)