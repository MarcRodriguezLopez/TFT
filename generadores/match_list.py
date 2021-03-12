import pandas as pd
import csv
import re

teams_dict = {}

def getDict(teams):
    df = pd.read_csv(teams)
    for i in range(len(df)):
        team = df["Team"][i]
        id = df["Id"][i]
        teams_dict[team] = format(id, '02d')


def parseCode(code):  # devuelve [fecha, equipo visitante, equipo local]
    date = code[:-6]
    vis = code[-6:-3]
    loc = code[-3:]
    resA = []
    resA.insert(len(resA), date[:4])
    resA.insert(len(resA), date[4:6])
    resA.insert(len(resA), date[6:8])
    resA.insert(len(resA), teams_dict[vis])
    resA.insert(len(resA), teams_dict[loc])
    return resA


def main(inputDoc, outputDoc, teams):
    with open(inputDoc) as dat_file, open(outputDoc, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Id", "Year", "Month", "Day", "Away", "Home"])
        matchslist = []
        i = 0
        getDict(teams)

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
            matchslist.insert(len(matchslist), code)
        matchslist = list(dict.fromkeys(matchslist))
        for n in matchslist:
            aux = parseCode(n)
            writer.writerow([i, aux[0], aux[1], aux[2], aux[3], aux[4]])
            i = i + 1