
import json

import pandas as pd
from numpy import *

from NBAstatsApp.models import Match, Team, Standing
from NBAstatsApp.backend import matchFormat, seasonFormat


def saveStanding(Smonth, Syear, Spart):
    for i in range(30):
        row_favor, row_contra, Steam, Snum_matches = getTeamStandingsMatches(i + 1, Spart, Smonth, Syear)
        row_favor_media = row_favor.mean()
        row_favor_media = row_favor_media.to_dict().values()
        row_favor_abs = row_favor.sum()
        row_favor_abs = row_favor_abs.to_dict().values()
        row_contra_media = row_contra.mean()
        row_contra_media = row_contra_media.to_dict().values()
        row_contra_abs = row_contra.sum()
        row_contra_abs = row_contra_abs.to_dict().values()
        jsonData = {
            'data_favor_media': [float('%.2f' % elem) for elem in list(row_favor_media)],
            'data_favor_abs': [float('%.2f' % elem) for elem in list(row_favor_abs)],
            'data_contra_media': [float('%.2f' % elem) for elem in list(row_contra_media)],
            'data_contra_abs': [float('%.2f' % elem) for elem in list(row_contra_abs)]
        }
        jsonData = json.dumps(jsonData)
        s = Standing(team=Steam, month=Smonth, year=Syear, part=Spart, num_matches=Snum_matches, data=jsonData)
        s.save()


def getTeamStandingsMatches(id, part, actualMonth, actualYear):
    if id == 2:
        team1 = Team.objects.get(id=2)
        team2 = Team.objects.get(id=34)
    elif id == 3:
        team1 = Team.objects.get(id=3)
        team2 = Team.objects.get(id=31)
    elif id == 4:
        team1 = Team.objects.get(id=4)
        team2 = Team.objects.get(id=35)
    elif id == 5:
        team1 = Team.objects.get(id=5)
        team2 = Team.objects.get(id=33)
    elif id == 7:
        team1 = Team.objects.get(id=7)
        team2 = Team.objects.get(id=32)
    elif id == 9:
        team1 = Team.objects.get(id=9)
        team2 = Team.objects.get(id=36)
    else:
        team1 = Team.objects.get(id=id)
        team2 = Team.objects.get(id=id)
    a = (Match.objects.filter(away=team1) | Match.objects.filter(home=team1) | Match.objects.filter(away=team2) |
         Match.objects.filter(home=team2)) & Match.objects.filter(month=actualMonth) & Match.objects.filter(
        year=actualYear)
    a = list(a)
    df_favor = pd.DataFrame(
        columns=['Points', 'FTM', 'FTA', 'FGM', 'FGA', '3PM', 'Assists', 'Turnovers', 'Steals', 'Blocks', 'Rebounds'])
    df_contra = pd.DataFrame(
        columns=['Points', 'FTM', 'FTA', 'FGM', 'FGA', '3PM', 'Assists', 'Turnovers', 'Steals', 'Blocks', 'Rebounds'])
    for match in range(len(a)):
        partido = a[match]
        b = json.loads(a[match].data)
        data = b[part]
        if partido.away == team1 or partido.away == team2:
            data_favor = matchFormat.getOneTeamData('away', data)
            data_contra = matchFormat.getOneTeamData('home', data)
        else:
            data_favor = matchFormat.getOneTeamData('home', data)
            data_contra = matchFormat.getOneTeamData('away', data)
        df_length = len(df_favor)
        df_favor.loc[df_length] = data_favor
        df_length = len(df_contra)
        df_contra.loc[df_length] = data_contra
    return df_favor, df_contra, team2, len(a)


def getListMonths(since, to):
    monthsData = [1, 2, 3, 4, 7, 10, 11, 12]
    yearsData = [2005, 2006, 2007, 2008, 2009, 2010]
    startYearsIndex = yearsData.index(since[1])
    endYearsIndex = yearsData.index(to[1])
    years = yearsData[startYearsIndex:endYearsIndex + 1]
    startMonthsIndex = monthsData.index(since[0])
    endMonthsIndex = monthsData.index(to[0])
    monthsStart = monthsData[startMonthsIndex:]
    monthsEnd = monthsData[:endMonthsIndex + 1]
    res = []
    if len(years) == 1:
        monthsStart_as_set = set(monthsStart)
        intersection = monthsStart_as_set.intersection(monthsEnd)
        a = list(intersection)
        a.sort()
        for i in a:
            res.append([i, years[0]])
        return res
    else:
        yearsBetween = len(years) - 2
        for i in monthsStart:
            res.append([i, years[0]])
        for x in range(yearsBetween):
            for m in monthsData:
                res.append([m, years[x + 1]])
        for i in monthsEnd:
            res.append([i, years[yearsBetween + 1]])
        return res


def getStandings(since, to, part, wl):
    months = getListMonths(since, to)
    res = {}
    dataFavorAbsList = []
    dataContraAbsList = []
    dataFavorAvgList = []
    dataContraAvgList = []
    for i in range(30):
        if i + 1 == 2:
            team = Team.objects.get(id=34)
        elif i + 1 == 3:
            team = Team.objects.get(id=31)
        elif i + 1 == 4:
            team = Team.objects.get(id=35)
        elif i + 1 == 5:
            team = Team.objects.get(id=33)
        elif i + 1 == 7:
            team = Team.objects.get(id=32)
        elif i + 1 == 9:
            team = Team.objects.get(id=36)
        else:
            team = Team.objects.get(id=i + 1)
        num_matches = 0
        dataFavor = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        dataContra = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for m in months:
            try:
                s = Standing.objects.get(team=team, month=m[0], year=m[1], part=part)
                num_matches = num_matches + s.num_matches
                obj = json.loads(s.data)
                dataFavor = [x + y for x, y in zip(dataFavor, obj['data_favor_abs'])]
                dataContra = [x + y for x, y in zip(dataContra, obj['data_contra_abs'])]
            except:
                pass
        dataFavorAvg = [float('%.2f' % (x / num_matches)) for x in dataFavor]
        dataContraAvg = [float('%.2f' % (x / num_matches)) for x in dataContra]
        if wl is True:
            wins, loses = getWinsPerYear(i, since[1], to[1])
            dataFavorAbsList.append([team.team, wins, loses] + dataFavor)
            dataContraAbsList.append([team.team, wins, loses] + dataContra)
            dataFavorAvgList.append([team.team, wins, loses] + dataFavorAvg)
            dataContraAvgList.append([team.team, wins, loses] + dataContraAvg)
        else:
            dataFavorAbsList.append([team.team] + dataFavor)
            dataContraAbsList.append([team.team] + dataContra)
            dataFavorAvgList.append([team.team] + dataFavorAvg)
            dataContraAvgList.append([team.team] + dataContraAvg)
    res['dataFavorAbs'] = dataFavorAbsList
    res['dataContraAbs'] = dataContraAbsList
    res['dataFavorAvg'] = dataFavorAvgList
    res['dataContraAvg'] = dataContraAvgList
    return res


def getTeamStandings(i, since, to):
    months = getListMonths(since, to)
    res = {}
    if i + 1 == 2:
        team = Team.objects.get(id=34)
    elif i + 1 == 3:
        team = Team.objects.get(id=31)
    elif i + 1 == 4:
        team = Team.objects.get(id=35)
    elif i + 1 == 5:
        team = Team.objects.get(id=33)
    elif i + 1 == 7:
        team = Team.objects.get(id=32)
    elif i + 1 == 9:
        team = Team.objects.get(id=36)
    else:
        team = Team.objects.get(id=i + 1)
    num_matches = 0
    dataFavor = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for m in months:
        try:
            s = Standing.objects.get(team=team, month=m[0], year=m[1], part='data')
            num_matches = num_matches + s.num_matches
            obj = json.loads(s.data)
            dataFavor = [x + y for x, y in zip(dataFavor, obj['data_favor_abs'])]
        except:
            pass
    dataFavorAvg = [float('%.2f' % (x / num_matches)) for x in dataFavor]
    res['dataFavorAbs'] = dataFavor
    res['dataFavorAvg'] = dataFavorAvg
    return res


def rankings(i, year1, year2, part):
    if i + 1 == 2:
        team = Team.objects.get(id=34)
    elif i + 1 == 3:
        team = Team.objects.get(id=31)
    elif i + 1 == 4:
        team = Team.objects.get(id=35)
    elif i + 1 == 5:
        team = Team.objects.get(id=33)
    elif i + 1 == 7:
        team = Team.objects.get(id=32)
    elif i + 1 == 9:
        team = Team.objects.get(id=36)
    else:
        team = Team.objects.get(id=i + 1)
    obj = getStandings(year1, year2, part, False)
    dataFavorAbs = obj['dataFavorAbs']
    dataFavorAvg = obj['dataFavorAvg']
    abs = {}
    avg = {}
    for i in range(30):
        abs[dataFavorAbs[i][0]] = dataFavorAbs[i][1:]
        avg[dataFavorAvg[i][0]] = dataFavorAvg[i][1:]
    dfAbs = pd.DataFrame.from_dict(abs, orient='index')
    dfAvg = pd.DataFrame.from_dict(avg, orient='index')
    dfAbs.columns = ['Points', 'FTM', 'FTA', 'FGM', 'FGA', '3PM', 'Assists', 'Turnovers', 'Steals', 'Blocks', 'Rebounds']
    dfAvg.columns = ['Points', 'FTM', 'FTA', 'FGM', 'FGA', '3PM', 'Assists', 'Turnovers', 'Steals', 'Blocks', 'Rebounds']
    res = {}
    for a in ['Points', 'FTM', 'FTA', 'FGM', 'FGA', '3PM', 'Assists', 'Turnovers', 'Steals', 'Blocks', 'Rebounds']:
        x = [(dfAvg.sort_values(by=[a], ascending=False)).index.get_loc(team.team),
             dfAvg._get_value(team.team, a),
             (dfAbs.sort_values(by=[a], ascending=False)).index.get_loc(team.team),
             dfAbs._get_value(team.team, a)]
        res[str(year2[1]) + a] = x
    return res

def getWinsPerYear(id, year, year2):
    resWins = 0
    resLoses = 0
    wins, loses = seasonFormat.getWinsPerMonth(id, 10, year)
    resWins = resWins + wins
    resLoses = resLoses + loses
    wins, loses = seasonFormat.getWinsPerMonth(id, 11, year)
    resWins = resWins + wins
    resLoses = resLoses + loses
    wins, loses = seasonFormat.getWinsPerMonth(id, 12, year)
    resWins = resWins + wins
    resLoses = resLoses + loses
    wins, loses = seasonFormat.getWinsPerMonth(id, 1, year2)
    resWins = resWins + wins
    resLoses = resLoses + loses
    wins, loses = seasonFormat.getWinsPerMonth(id, 2, year2)
    resWins = resWins + wins
    resLoses = resLoses + loses
    wins, loses = seasonFormat.getWinsPerMonth(id, 3, year2)
    resWins = resWins + wins
    resLoses = resLoses + loses
    wins, loses = seasonFormat.getWinsPerMonth(id, 4, year2)
    resWins = resWins + wins
    resLoses = resLoses + loses
    return resWins, resLoses

def getColor(id):
    if id is 0:
        return '#1d1160'
    elif id is 1:
        return '#EF426F'
    elif id is 2:
        return '#006bb6'
    elif id is 3:
        return '#0C2340'
    elif id is 4:
        return '#ffc72c'
    elif id is 5:
        return '#CE1141'
    elif id is 6:
        return '#00471B'
    elif id is 7:
        return '#0077c0'
    elif id is 8:
        return '#ef3b24'
    elif id is 9:
        return '#8B2131'
    elif id is 10:
        return '#5D76A9'
    elif id is 11:
        return '#000000'
    elif id is 12:
        return '#007A33'
    elif id is 13:
        return '#860038'
    elif id is 14:
        return '#C8102E'
    elif id is 15:
        return '#0C2340'
    elif id is 16:
        return '#C4CED4'
    elif id is 17:
        return '#B4975A'
    elif id is 18:
        return '#98002E'
    elif id is 19:
        return '#552583'
    elif id is 20:
        return '#1d428a'
    elif id is 21:
        return '#F58426'
    elif id is 22:
        return '#E03A3E'
    elif id is 23:
        return '#00788C'
    elif id is 24:
        return '#00471B'
    elif id is 25:
        return '#002B5C'
    elif id is 26:
        return '#FDBB30'
    elif id is 27:
        return '#00538C'
    elif id is 28:
        return '#5a2d81'
    elif id is 29:
        return '#C1D32F'

def getName(team):
    if team == 'PHL':
        return 'PHI'
    elif team == 'UTH':
        return 'UTA'
    elif team == 'GOS':
        return 'GSW'
    elif team == 'NOK':
        return 'NOP'
    elif team == 'SEA':
        return 'OKC'
    elif team == 'SAN':
        return 'SAS'
    elif team == 'NJN':
        return 'BKN'
    else:
        return team

def getVersusData(teams, target, year):
    targetDataMediaDict = {}
    targetDataMediaList = []
    teamsList = []
    colorsList = []
    for team in teams:
        obj = seasonFormat.getMonthsPerYear(team, year - 1, year)
        t = Team.objects.get(id=team+1)
        targetDataMedia = [
            (obj['octubre_media'])[target],
            (obj['noviembre_media'])[target],
            (obj['diciembre_media'])[target],
            (obj['enero_media'])[target],
            (obj['febrero_media'])[target],
            (obj['marzo_media'])[target],
            (obj['abril_media'])[target]
        ]
        for numeric_string in range(len(targetDataMedia)):
            if math.isnan(targetDataMedia[numeric_string]):
                targetDataMedia[numeric_string] = 0
        targetDataMediaList.append(targetDataMedia)
        teamsList.append(getName(str(t.team)))
        colorsList.append(getColor(team))
    targetDataMediaDict['data'] = targetDataMediaList
    targetDataMediaDict['teams'] = teamsList
    targetDataMediaDict['colors'] = colorsList
    return targetDataMediaDict