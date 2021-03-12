# import csv
# import os
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "NBAstats.settings")
# import django
# django.setup()
# import pandas as pd
import json
# Set path of new directory here
# os.chdir('G:\\TFG\\NBAstats\\generadores') # changes the directory
from NBAstatsApp.models import Match  # imports the model

# df = pd.read_csv('teamsFile.csv')
# for x in range(len(df)):
#     p = Team(team=df['Team'][x], id=df['Id'][x])
#     p.save()

# df = pd.read_csv('matchsFile.csv')
# for x in range(6133):
#     a = df[df['Id'] == x]
#     jsonData = {'data' : a.iloc[0].tolist()[7:]}
#     jsonData = json.dumps(jsonData)
#     away_t = Team.objects.get(id=a['Away'])
#     home_t = Team.objects.get(id=a['Home'])
#     p = Match(id=a['Id'], year=a['Year'], month=a['Month'],
#     day=a['Day'], away=away_t, home=home_t, ot=int(float(a['OverTime'])), data=jsonData)
#     p.save()

# for x in range(6133):
#     m = Match.objects.get(id=x)
#     obj = json.loads(m.data)
#     obj = obj['data']
#     obj[6] = obj[6] + obj[10]
#     obj[8] = obj[8] + obj[10]
#     obj[7] = obj[7] + obj[11]
#     obj[9] = obj[9] + obj[11]
#     jsonData = {'data': obj}
#     jsonData = json.dumps(jsonData)
#     m.data = jsonData
#     m.save()

# lol = json.loads(jsonData)
# print(lol['data'])


# df = pd.read_csv('assistsFile.csv')
# for x in range(6133):
#     a = df[df['Code'] == x]
#     time_a = a['Time'].tolist()
#     team_a = a['Team'].tolist()
#     points_a = a['PointsGenerated'].tolist()
#     jsonData = {'time': time_a,
#                 'team': team_a,
#                 'pointsGenerated': points_a}
#     jsonData = json.dumps(jsonData)
#     match = Match.objects.get(id=x)
#     p = Assist(code=match, data=jsonData)
#     p.save()


# Code,Time,Team,Steal,Block,Rebound

# df = pd.read_csv('SBRFile.csv')
# for x in range(6133):
#     a = df[df['Code'] == x]
#     a = a[a['Block'] == 1]
#     time_a = a['Time'].tolist()
#     team_a = a['Team'].tolist()
#     jsonData = {'time': time_a,
#                 'team': team_a}
#     jsonData = json.dumps(jsonData)
#     match = Match.objects.get(id=x)
#     p = Block(code=match, data=jsonData)
#     p.save()

# df = pd.read_csv('SBRFile.csv')
# for x in range(6133):
#     a = df[df['Code'] == x]
#     a = a[a['Steal'] == 1]
#     time_a = a['Time'].tolist()
#     team_a = a['Team'].tolist()
#     jsonData = {'time': time_a,
#                 'team': team_a}
#     jsonData = json.dumps(jsonData)
#     match = Match.objects.get(id=x)
#     p = Steal(code=match, data=jsonData)
#     p.save()

# df = pd.read_csv('SBRFile.csv')
# for x in range(6133):
#     a = df[df['Code'] == x]
#     a = a[a['Rebound'] == 1]
#     time_a = a['Time'].tolist()
#     team_a = a['Team'].tolist()
#     jsonData = {'time': time_a,
#                 'team': team_a}
#     jsonData = json.dumps(jsonData)
#     match = Match.objects.get(id=x)
#     p = Rebound(code=match, data=jsonData)
#     p.save()

# df = pd.read_csv('foulsFile.csv')
# for x in range(6133):
#     a = df[df['Code'] == x]
#     time_a = a['Time'].tolist()
#     team_a = a['Team'].tolist()
#     points_a = a['FoulType'].tolist()
#     jsonData = {'time': time_a,
#                 'team': team_a,
#                 'foulType': points_a}
#     jsonData = json.dumps(jsonData)
#     match = Match.objects.get(id=x)
#     p = Foul(code=match, data=jsonData)
#     p.save()

# df = pd.read_csv('pointsFile.csv')
# for x in range(6133):
#     a = df[df['Code'] == x]
#     time_a = a['Time'].tolist()
#     team_a = a['Team'].tolist()
#     type_a = a['TypeShot'].tolist()
#     value_a = a['Value'].tolist()
#     jsonData = {'time': time_a,
#                 'team': team_a,
#                 'foulType': type_a,
#                 'value': value_a}
#     jsonData = json.dumps(jsonData)
#     match = Match.objects.get(id=x)
#     p = Point(code=match, data=jsonData)
#     p.save()

# df = pd.read_csv('substitutionsFile.csv')
# for x in range(6133):
#     a = df[df['Code'] == x]
#     time_a = a['Time'].tolist()
#     team_a = a['Team'].tolist()
#     number_a = a['Number'].tolist()
#     jsonData = {'time': time_a,
#                 'team': team_a,
#                 'number': number_a}
#     jsonData = json.dumps(jsonData)
#     match = Match.objects.get(id=x)
#     p = Substitution(code=match, data=jsonData)
#     p.save()


# df = pd.read_csv('turnoversFile.csv')
# for x in range(6133):
#     a = df[df['Code'] == x]
#     time_a = a['Time'].tolist()
#     team_a = a['Team'].tolist()
#     number_a = a['FoulType'].tolist()
#     jsonData = {'time': time_a,
#                 'team': team_a,
#                 'type': number_a}
#     jsonData = json.dumps(jsonData)
#     match = Match.objects.get(id=x)
#     p = Turnover(code=match, data=jsonData)
#     p.save()

# df = pd.read_csv('listsFile.csv')
# for x in range(len(df)):
#     p = Type(action=df['Action'][x], code=df['Id'][x], clase=df['Type'][x])
#     p.save()


#
# df1 = pd.read_csv('assistsFile.csv')
# df1 = df1[df1['Code'] == 152]
# time_a = df1['Time'].tolist()
# team_a = df1['Team'].tolist()
# points_a = df1['PointsGenerated'].tolist()
# print('{} - {} - {}'.format(len(a), len(b), len(c)))


# Match(id=row['Id'], year=row['Year'], month=row['Month'],
#   day=row['Day'], away=away_t, home=home_t, ot=int(float(row['OverTime'])),
#   awayPoints=int(float(row['AwayPoints'])), homePoints=int(float(row['HomePoints'])),
#   awayFTM=int(float(row['AwayFTM'])), homeFTM=int(float(row['HomeFTM'])), awayFTA=int(float(row['AwayFTA'])),
#   homeFTA=int(float(row['HomeFTA'])), awayFGM=int(float(row['AwayFGM'])), homeFGM=int(float(row['HomeFGM'])),
#   awayFGA=int(float(row['AwayFGA'])), homeFGA=int(float(row['HomeFGA'])), away3PM=int(float(row['Away3PM'])),
#   home3PM=int(float(row['Home3PM'])), awayAssists=int(float(row['AwayAssists'])),
#   homeAssists=int(float(row['HomeAssists'])), awayTurnovers=int(float(row['AwayTurnovers'])),
#   homeTurnovers=int(float(row['HomeTurnovers'])), awaySteals=int(float(row['AwaySteals'])),
#   homeSteals=int(float(row['HomeSteals'])), awayBlocks=int(float(row['AwayBlocks'])),
#   homeBlocks=int(float(row['HomeBlocks'])), awayRebounds=int(float(row['AwayRebounds'])),
#   homeRebounds=int(float(row['HomeRebounds'])))
