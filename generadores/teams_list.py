import csv
import re


def main(inputDoc, outputDoc):
    with open(inputDoc) as dat_file, open(outputDoc, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        teamslist = []

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


            team = code.strip()[-3:]
            if len(team) == 3:
                teamslist.insert(len(teamslist), team)
        teamslist = list(dict.fromkeys(teamslist))
        i = 1
        writer.writerow(["Team", "Id"])
        for n in teamslist:
            if i < 10:
                writer.writerow([n, format(i, '02d')])
            else:
                writer.writerow([n, i])
            i = i + 1