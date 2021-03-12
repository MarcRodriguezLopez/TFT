import pandas as pd
import re
import csv

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


def fillFile(code, time, fact, writer_st_bl):
    if "Rebound" in fact:
        writer_st_bl.writerow([code, time, getTeam(fact), 0, 0, 1])
    elif "Steal" in fact:
        writer_st_bl.writerow([code, time, getTeam(fact), 1, 0, 0])
    elif "Block" in fact:
        writer_st_bl.writerow([code, time, getTeam(fact), 0, 1, 0])


def main(inputDoc, outputDoc, teams, matchs):
    with open(inputDoc) as dat_file, open(outputDoc, 'w', newline='') as csv_file_st_bl_rb:
        writer_st_bl = csv.writer(csv_file_st_bl_rb)
        writer_st_bl.writerow(['Code', 'Time', 'Team', 'Steal', 'Block', 'Rebound'])

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
            fillFile(parseCode(code), time.strip(), fact, writer_st_bl)