import json

import pandas as pd

from NBAstatsApp.models import Team, Assist, Match, Point, Steal, Substitution, Rebound, Turnover, Block, Foul, Type


def resizeDataFrameWithTime(match, df, since, to):
    # miramos si hay prorroga para poder coger la prorroga como el tercer tiempo, se tiene que coger a parte por el signo negativo del tiempo
    if match.ot == 1:
        OT = df[df['time'].astype(str).str.contains("-")]
        df = df[~df['time'].astype(str).str.contains("-")]
        OT['seconds'] = 0 - (OT['time'].astype(str).str[4:6].astype(int) * 60 + OT['time'].astype(str).str[7:9].astype(int))
        df['seconds'] = df['time'].astype(str).str[3:5].astype(int) * 60 + df['time'].astype(str).str[6:8].astype(int)
        frames = [df, OT]
        df = pd.concat(frames)
    else:
        df['seconds'] = df['time'].astype(str).str[3:5].astype(int) * 60 + df['time'].astype(str).str[6:8].astype(int)

    # aqui tenemos las mascaras de las dos medias partes, antes hemos creado el campo seconds que es el time en segundos
    if len(since) == 6:
        since = 0 - (int(since[1:3]) * 60 + int(since[4:6]))
    else:
        since = int(since[0:2]) * 60 + int(since[3:5])
    to = int(to[0:2]) * 60 + int(to[3:5])
    mask = (df['seconds'] > since) & (df['seconds'] < to)
    return df[mask]


def getPointValues(match, df):
    awayMask = df['team'] == match.away.id
    homeMask = df['team'] == match.home.id
    awayObj = df[awayMask]
    homeObj = df[homeMask]
    try:
        awayFTM = awayObj['value'].value_counts()[1]
    except:
        awayFTM = 0
    try:
        away3PM = awayObj['value'].value_counts()[3]
    except:
        away3PM = 0
    try:
        awayFGM = awayObj['value'].value_counts()[2] + away3PM
    except:
        awayFGM = away3PM
    try:
        awayFTA = awayObj['foulType'].value_counts()[67]
    except:
        awayFTA = 0
    fallosFT = awayFTA - awayFTM
    try:
        fallosFG = awayObj['value'].value_counts()[0] - fallosFT
    except:
        fallosFG = 0
    awayFGA = fallosFG + awayFGM
    awayPoints = awayFTM + away3PM + (awayFGM * 2)

    try:
        homeFTM = homeObj['value'].value_counts()[1]
    except:
        homeFTM = 0
    try:
        home3PM = homeObj['value'].value_counts()[3]
    except:
        home3PM = 0
    try:
        homeFGM = homeObj['value'].value_counts()[2] + home3PM
    except:
        homeFGM = home3PM
    try:
        homeFTA = homeObj['foulType'].value_counts()[67]
    except:
        homeFTA = 0
    fallosFT = homeFTA - homeFTM
    try:
        fallosFG = homeObj['value'].value_counts()[0] - fallosFT
    except:
        fallosFG = 0
    homeFGA = fallosFG + homeFGM
    homePoints = homeFTM + home3PM + (homeFGM * 2)
    return [awayPoints, homePoints, awayFTM, homeFTM, awayFTA, homeFTA, awayFGM, homeFGM, awayFGA, homeFGA, away3PM,
            home3PM]


def getRestValues(match, df):
    try:
        home = df['team'].value_counts()[match.home.id]
    except:
        home = 0
    try:
        away = df['team'].value_counts()[match.away.id]
    except:
        away = 0
    return [away, home]


def matchFromTime(a, since, to):
    match = Match.objects.get(id=a)
    # Points
    pointModel = Point.objects.get(code=match)
    obj = json.loads(pointModel.data)
    pointsDF = pd.DataFrame.from_dict(obj)

    pointsDF = resizeDataFrameWithTime(match, pointsDF, since, to)
    pointsData = getPointValues(match, pointsDF)

    # Assists
    assistsModel = Assist.objects.get(code=match)
    obj = json.loads(assistsModel.data)
    assistsDF = pd.DataFrame.from_dict(obj)

    assistsDF = resizeDataFrameWithTime(match, assistsDF, since, to)
    assistsData = getRestValues(match, assistsDF)

    # Turnovers
    turnoversModel = Turnover.objects.get(code=match)
    obj = json.loads(turnoversModel.data)
    turnoverDF = pd.DataFrame.from_dict(obj)

    turnoverDF = resizeDataFrameWithTime(match, turnoverDF, since, to)
    turnoverData = getRestValues(match, turnoverDF)

    # Steals
    stealsModel = Steal.objects.get(code=match)
    obj = json.loads(stealsModel.data)
    stealsDF = pd.DataFrame.from_dict(obj)

    stealsDF = resizeDataFrameWithTime(match, stealsDF, since, to)
    stealsData = getRestValues(match, stealsDF)

    # Blocks
    blocksModel = Block.objects.get(code=match)
    obj = json.loads(blocksModel.data)
    blocksDF = pd.DataFrame.from_dict(obj)

    blocksDF = resizeDataFrameWithTime(match, blocksDF, since, to)
    blocksData = getRestValues(match, blocksDF)

    # Rebounds
    reboundsModel = Rebound.objects.get(code=match)
    obj = json.loads(reboundsModel.data)
    reboundsDF = pd.DataFrame.from_dict(obj)

    reboundsDF = resizeDataFrameWithTime(match, reboundsDF, since, to)
    reboundsData = getRestValues(match, reboundsDF)

    results = pointsData + assistsData + turnoverData + stealsData + blocksData + reboundsData
    results = [float(i) for i in results]
    obj = {"data": results}
    away = str(match.away)
    obj['awayTeam'] = away
    home = str(match.home)
    obj['homeTeam'] = home
    date = str(match.day) + '/' + str(match.month) + '/' + str(match.year)
    obj['date'] = date
    return obj


def matchFull(a):
    match = Match.objects.get(id=a)
    obj = json.loads(match.data)
    away = str(match.away)
    obj['awayTeam'] = away
    home = str(match.home)
    obj['homeTeam'] = home
    date = str(match.day) + '/' + str(match.month) + '/' + str(match.year)
    obj['date'] = date
    # obj['data1qtr'] = matchFromTime(a, '36:00', '48:00')['data']
    # obj['data2qtr'] = matchFromTime(a, '24:00', '36:00')['data']
    # obj['data3qtr'] = matchFromTime(a, '12:00', '24:00')['data']
    # obj['data4qtr'] = matchFromTime(a, '00:00', '12:00')['data']
    # obj['data1hlf'] = matchFromTime(a, '24:00', '48:00')['data']
    # obj['data2hlf'] = matchFromTime(a, '00:00', '24:00')['data']
    # match.data = json.dumps(obj)
    # match.save()
    return obj


def getOneTeamData(team, dataMatch):
    if team == 'away':
        return dataMatch[::2]
    else:
        return dataMatch[1::2]

def getMatchId(idTeam, day, month, year):
    if idTeam + 1 == 2:
        team1 = Team.objects.get(id=2)
        team2 = Team.objects.get(id=34)
    elif idTeam + 1 == 3:
        team1 = Team.objects.get(id=3)
        team2 = Team.objects.get(id=31)
    elif idTeam + 1 == 4:
        team1 = Team.objects.get(id=4)
        team2 = Team.objects.get(id=35)
    elif idTeam + 1 == 5:
        team1 = Team.objects.get(id=5)
        team2 = Team.objects.get(id=33)
    elif idTeam + 1 == 7:
        team1 = Team.objects.get(id=7)
        team2 = Team.objects.get(id=32)
    elif idTeam + 1 == 9:
        team1 = Team.objects.get(id=9)
        team2 = Team.objects.get(id=36)
    else:
        team1 = Team.objects.get(id=idTeam + 1)
        team2 = Team.objects.get(id=idTeam + 1)
    try:
        return Match.objects.get(away=team1, day=day, month=month, year=year)
    except:
        pass
    try:
        return Match.objects.get(away=team2, day=day, month=month, year=year)
    except:
        pass
    try:
        return Match.objects.get(home=team1, day=day, month=month, year=year)
    except:
        pass
    try:
        return Match.objects.get(home=team2, day=day, month=month, year=year)
    except:
        pass
    team = Team.objects.get(id=1)
    a= Match.objects.filter(home=team, day=1, month=11, year=2005)
    return a