import json

import pandas as pd
import datetime

from NBAstatsApp.models import Match, Team, Standing
from NBAstatsApp.backend import matchFormat


def setDates(df, since, to):
    since_day=since[0:2]
    since_month=since[3:5]
    since_year=since[6:10]
    to_day=to[0:2]
    to_month=to[3:5]
    to_year=to[6:10]
    since_date = datetime.datetime(int(since_year), int(since_month), int(since_day))
    to_date = datetime.datetime(int(to_year), int(to_month), int(to_day))
    df['Date'] = pd.to_datetime(df[['Year', 'Month', 'Day']])
    df = df.drop(columns=['Year', 'Month', 'Day'])
    mask = (df['Date'] >= since_date) & (df['Date'] <= to_date)
    return df[mask].sort_values(by='Date')

def getTeamMatches(id, since, to, type):
    if id + 1 == 2:
        team1 = Team.objects.get(id=2)
        team2 = Team.objects.get(id=34)
        a = Match.objects.filter(away=team1) | Match.objects.filter(home=team1) | Match.objects.filter(
            away=team2) | Match.objects.filter(home=team2)
        a = list(a)
    elif id + 1 == 3:
        team1 = Team.objects.get(id=3)
        team2 = Team.objects.get(id=31)
        a = Match.objects.filter(away=team1) | Match.objects.filter(home=team1) | Match.objects.filter(
            away=team2) | Match.objects.filter(home=team2)
        a = list(a)
    elif id + 1 == 4:
        team1 = Team.objects.get(id=4)
        team2 = Team.objects.get(id=35)
        a = Match.objects.filter(away=team1) | Match.objects.filter(home=team1) | Match.objects.filter(
            away=team2) | Match.objects.filter(home=team2)
        a = list(a)
    elif id + 1 == 5:
        team1 = Team.objects.get(id=5)
        team2 = Team.objects.get(id=33)
        a = Match.objects.filter(away=team1) | Match.objects.filter(home=team1) | Match.objects.filter(
            away=team2) | Match.objects.filter(home=team2)
        a = list(a)
    elif id + 1 == 7:
        team1 = Team.objects.get(id=7)
        team2 = Team.objects.get(id=32)
        a = Match.objects.filter(away=team1) | Match.objects.filter(home=team1) | Match.objects.filter(
            away=team2) | Match.objects.filter(home=team2)
        a = list(a)
    elif id + 1 == 9:
        team1 = Team.objects.get(id=9)
        team2 = Team.objects.get(id=36)
        a = Match.objects.filter(away=team1) | Match.objects.filter(home=team1) | Match.objects.filter(
            away=team2) | Match.objects.filter(home=team2)
        a = list(a)
    else:
        team1 = Team.objects.get(id=id)
        team2 = Team.objects.get(id=id)
        a = Match.objects.filter(away=team1) | Match.objects.filter(home=team1) | Match.objects.filter(
            away=team2) | Match.objects.filter(home=team2)
        a = list(a)
    df = pd.DataFrame(
        columns=['Year', 'Month', 'Day', 'Team', 'Points', 'FTM', 'FTA', 'FGM', 'FGA', '3PM', 'Assists', 'Turnovers', 'Steals', 'Blocks',
                 'Rebounds'])
    for match in range(len(a)):
        partido = a[match]
        year = partido.year
        month = partido.month
        day = partido.day
        b = json.loads(a[match].data)
        data = b['data']
        if partido.away == team1 or partido.away == team2:
            data = matchFormat.getOneTeamData('away', data)
            team = 'at ' + str(partido.home)
        else:
            data = matchFormat.getOneTeamData('home', data)
            team = 'vs ' + str(partido.away)
        df_length = len(df)
        df.loc[df_length] = [year, month, day] + [team] + data
    df = setDates(df, since, to)
    if type is 'json':
        df['Date'] = df['Date'].apply(lambda x: x.strftime('%Y-%m-%d'))
        df = df[['Date', 'Team', 'Points', 'FTM', 'FTA', 'FGM', 'FGA', '3PM', 'Assists', 'Turnovers', 'Steals', 'Blocks', 'Rebounds']]
        result = df.to_json(orient='split')
        parsed = json.loads(result)
        return parsed, str(team1)
    df = df[['Points', 'FTM', 'FTA', 'FGM', 'FGA', '3PM', 'Assists', 'Turnovers', 'Steals', 'Blocks', 'Rebounds']]
    return df


def getTeamMonthMatches(id, actualMonth, actualYear):
    if id + 1 == 2:
        team1 = Team.objects.get(id=2)
        team2 = Team.objects.get(id=34)
    elif id + 1 == 3:
        team1 = Team.objects.get(id=3)
        team2 = Team.objects.get(id=31)
    elif id + 1 == 4:
        team1 = Team.objects.get(id=4)
        team2 = Team.objects.get(id=35)
    elif id + 1 == 5:
        team1 = Team.objects.get(id=5)
        team2 = Team.objects.get(id=33)
    elif id + 1 == 7:
        team1 = Team.objects.get(id=7)
        team2 = Team.objects.get(id=32)
    elif id + 1 == 9:
        team1 = Team.objects.get(id=9)
        team2 = Team.objects.get(id=36)
    else:
        team1 = Team.objects.get(id=id + 1)
        team2 = Team.objects.get(id=id + 1)
    a = (Match.objects.filter(away=team1) | Match.objects.filter(home=team1) | Match.objects.filter(away=team2) |
         Match.objects.filter(home=team2)) & Match.objects.filter(month=actualMonth) & Match.objects.filter(year=actualYear)
    a = list(a)
    df_res = pd.DataFrame(columns=['day', 'win', 'result'])
    for match in range(len(a)):
        partido = a[match]
        b = json.loads(a[match].data)
        # Away,Home
        data = b['data']
        if partido.away == team1 or partido.away == team2:
            txt = str(int(data[0])) + '-' + str(int(data[1]))
            if data[0] > data[1]:
                win = 1
            else:
                win = 0
            df_res.loc[len(df_res)] = [partido.day, win, txt]
        else:
            txt = str(int(data[0])) + '-' + str(int(data[1]))
            if data[0] < data[1]:
                win = 1
            else:
                win = 0
            df_res.loc[len(df_res)] = [partido.day, win, txt]
    df_res = df_res.sort_values(by=['day'])
    result = {}
    result['days'] = df_res['day'].tolist()
    result['wins'] = df_res['win'].tolist()
    result['results'] = df_res['result'].tolist()
    return result

def getMonthsPerYear(id, year, year2):
    res = {}
    if id + 1 == 2:
        team = Team.objects.get(id=34)
    elif id + 1 == 3:
        team = Team.objects.get(id=31)
    elif id + 1 == 4:
        team = Team.objects.get(id=35)
    elif id + 1 == 5:
        team = Team.objects.get(id=33)
    elif id + 1 == 7:
        team = Team.objects.get(id=32)
    elif id + 1 == 9:
        team = Team.objects.get(id=36)
    else:
        team = Team.objects.get(id=id + 1)
    s = Standing.objects.get(team=team, month=1, year=year2, part='data')
    obj = json.loads(s.data)
    abs = obj['data_favor_abs']
    media = obj['data_favor_media']
    res['enero_abs'] = abs
    res['enero_media'] = media
    wins, loses = getWinsPerMonth(id, 1, year2)
    res['enero_matches'] = [wins, loses]
    s = Standing.objects.get(team=team, month=2, year=year2, part='data')
    obj = json.loads(s.data)
    abs = obj['data_favor_abs']
    media = obj['data_favor_media']
    res['febrero_abs'] = abs
    res['febrero_media'] = media
    wins, loses = getWinsPerMonth(id, 2, year2)
    res['febrero_matches'] = [wins, loses]
    s = Standing.objects.get(team=team, month=3, year=year2, part='data')
    obj = json.loads(s.data)
    abs = obj['data_favor_abs']
    media = obj['data_favor_media']
    res['marzo_abs'] = abs
    res['marzo_media'] = media
    wins, loses = getWinsPerMonth(id, 3, year2)
    res['marzo_matches'] = [wins, loses]
    s = Standing.objects.get(team=team, month=4, year=year2, part='data')
    obj = json.loads(s.data)
    abs = obj['data_favor_abs']
    media = obj['data_favor_media']
    res['abril_abs'] = abs
    res['abril_media'] = media
    wins, loses = getWinsPerMonth(id, 4, year2)
    res['abril_matches'] = [wins, loses]
    try:
        s = Standing.objects.get(team=team, month=10, year=year, part='data')
        obj = json.loads(s.data)
        abs = obj['data_favor_abs']
        media = obj['data_favor_media']
        wins, loses = getWinsPerMonth(id, 10, year)
        res['octubre_matches'] = [wins, loses]
    except:
        abs = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        media = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        res['octubre_matches'] = [0, 0]
    res['octubre_abs'] = abs
    res['octubre_media'] = media
    s = Standing.objects.get(team=team, month=11, year=year, part='data')
    obj = json.loads(s.data)
    abs = obj['data_favor_abs']
    media = obj['data_favor_media']
    res['noviembre_abs'] = abs
    res['noviembre_media'] = media
    wins, loses = getWinsPerMonth(id, 11, year)
    res['noviembre_matches'] = [wins, loses]
    s = Standing.objects.get(team=team, month=12, year=year, part='data')
    obj = json.loads(s.data)
    abs = obj['data_favor_abs']
    media = obj['data_favor_media']
    res['diciembre_abs'] = abs
    res['diciembre_media'] = media
    wins, loses = getWinsPerMonth(id, 12, year)
    res['diciembre_matches'] = [wins, loses]
    return res

def getWinsPerMonth(id, month, year):
    res = getTeamMonthMatches(id, month, year)
    l = res['wins']
    return l.count(1), l.count(0)