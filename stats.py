import pandas as pd
from datetime import datetime
import datetime
import openpyxl



# con df[mask] obtenemos los partidos entre ambas fechas

def getStatsMatchsFile(diferencia, teams, result, df):
    # diferencia:
    # 0 si es todos los partidos
    # 1 si es mayor de 12 puntos
    # 2 si es menor de 12 puntos
    # teams:
    # 0 si son ambos equios
    # 1 si es el equipo local(home)
    # 2 si es el equipo visitante(away)
    # result:
    # 0 si son ambos
    # 1 si son los ganadores
    # 2 si son los perdedores





    if (diferencia == 1):
        mask = ((df['AwayPoints'] - df['HomePoints']).abs()) > 12
        df = df[mask]
    elif (diferencia == 2):
        mask = ((df['AwayPoints'] - df['HomePoints']).abs()) < 12
        df = df[mask]

    a_mask = df['AwayPoints'] < df['HomePoints']
    a = (df[a_mask])#[['AwayPoints', 'HomePoints']]
    away_lose_home_win = a.rename(columns={"Away": "Lose", "Home": "Win",
                                           "AwayPoints": "LosePoints", "HomePoints": "WinPoints",
                                           "AwayFTM": "LoseFTM", "HomeFTM": "WinFTM",
                                           "AwayFTA": "LoseFTA", "HomeFTA": "WinFTA",
                                           "AwayFGM": "LoseFGM", "HomeFGM": "WinFGM",
                                           "AwayFGA": "LoseFGA", "HomeFGA": "WinFGA",
                                           "Away3PM": "Lose3PM", "Home3PM": "Win3PM",
                                           "AwayAssists": "LoseAssists", "HomeAssists": "WinAssists",
                                           "AwayTurnovers": "LoseTurnovers", "HomeTurnovers": "WinTurnovers",
                                           "AwaySteals": "LoseSteals", "HomeSteals": "WinSteals",
                                           "AwayBlocks": "LoseBlocks", "HomeBlocks": "WinBlocks",
                                           "AwayRebounds": "LoseRebounds", "HomeRebounds": "WinRebounds"})

    b_mask = df['AwayPoints'] > df['HomePoints']
    b = (df[b_mask])#[['AwayPoints', 'HomePoints']]
    away_win_home_lose = b.rename(columns={"Away": "Win", "Home": "Lose",
                                           "AwayPoints": "WinPoints", "HomePoints": "LosePoints",
                                           "AwayFTM": "WinFTM", "HomeFTM": "LoseFTM",
                                           "AwayFTA": "WinFTA", "HomeFTA": "LoseFTA",
                                           "AwayFGM": "WinFGM", "HomeFGM": "LoseFGM",
                                           "AwayFGA": "WinFGA", "HomeFGA": "LoseFGA",
                                           "Away3PM": "Win3PM", "Home3PM": "Lose3PM",
                                           "AwayAssists": "WinAssists", "HomeAssists": "LoseAssists",
                                           "AwayTurnovers": "WinTurnovers", "HomeTurnovers": "LoseTurnovers",
                                           "AwaySteals": "WinSteals", "HomeSteals": "LoseSteals",
                                           "AwayBlocks": "WinBlocks", "HomeBlocks": "LoseBlocks",
                                           "AwayRebounds": "WinRebounds", "HomeRebounds": "LoseRebounds"})

    if (result == 0):
        if (teams == 1):
            df = df[['HomePoints', 'HomeFTM', 'HomeFTA', 'HomeFGM', 'HomeFGA', 'Home3PM', 'HomeAssists', 'HomeTurnovers', 'HomeSteals', 'HomeBlocks', 'HomeRebounds']]
        elif (teams == 2):
            df = df[['AwayPoints', 'AwayFTM', 'AwayFTA', 'AwayFGM', 'AwayFGA', 'Away3PM', 'AwayAssists', 'AwayTurnovers', 'AwaySteals', 'AwayBlocks', 'AwayRebounds']]
    else:
        if (teams == 0):
            frames = [away_lose_home_win, away_win_home_lose]
            conframes = pd.concat(frames)
            df = conframes.sort_index()
            if (result == 1):
                df = df[['WinPoints', 'WinFTM', 'WinFTA', 'WinFGM', 'WinFGA', 'Win3PM', 'WinAssists', 'WinTurnovers', 'WinSteals', 'WinBlocks', 'WinRebounds']]
            elif (result ==2):
                df = df[['LosePoints', 'LoseFTM', 'LoseFTA', 'LoseFGM', 'LoseFGA', 'Lose3PM', 'LoseAssists', 'LoseTurnovers', 'LoseSteals', 'LoseBlocks', 'LoseRebounds']]
        elif (teams == 1):#home
            if (result == 1):
                df = away_lose_home_win[['WinPoints', 'WinFTM', 'WinFTA', 'WinFGM', 'WinFGA', 'Win3PM', 'WinAssists', 'WinTurnovers', 'WinSteals', 'WinBlocks', 'WinRebounds']]
            elif (result ==2):
                df = away_win_home_lose[['LosePoints', 'LoseFTM', 'LoseFTA', 'LoseFGM', 'LoseFGA', 'Lose3PM', 'LoseAssists', 'LoseTurnovers', 'LoseSteals', 'LoseBlocks', 'LoseRebounds']]
        elif (teams == 2):#away
            if (result == 1):
                df = away_win_home_lose[['WinPoints', 'WinFTM', 'WinFTA', 'WinFGM', 'WinFGA', 'Win3PM', 'WinAssists', 'WinTurnovers', 'WinSteals', 'WinBlocks', 'WinRebounds']]
            elif (result ==2):
                df = away_lose_home_win[['LosePoints', 'LoseFTM', 'LoseFTA', 'LoseFGM', 'LoseFGA', 'Lose3PM', 'LoseAssists', 'LoseTurnovers', 'LoseSteals', 'LoseBlocks', 'LoseRebounds']]
    print(diferencia, teams, result, len(df))
    media = df.mean().to_dict()
    desviacion = df.std(axis=0).to_dict()
    res = [media, desviacion, len(df)]
    return res


def ficheros(df, fileName):
    mas_away_wins = getStatsMatchsFile(1, 2, 1, df)  # mas de 12, away, wins
    mas_away_loses = getStatsMatchsFile(1, 2, 2, df)
    mas_away_all = getStatsMatchsFile(1, 2, 0, df)
    mas_home_wins = getStatsMatchsFile(1, 1, 1, df)
    mas_home_loses = getStatsMatchsFile(1, 1, 2, df)
    mas_home_all = getStatsMatchsFile(1, 1, 0, df)
    mas_all_wins = getStatsMatchsFile(1, 0, 1, df)
    mas_all_loses = getStatsMatchsFile(1, 0, 2, df)
    menos_away_wins = getStatsMatchsFile(2, 2, 1, df)
    menos_away_loses = getStatsMatchsFile(2, 2, 2, df)
    menos_away_all = getStatsMatchsFile(2, 2, 0, df)
    menos_home_wins = getStatsMatchsFile(2, 1, 1, df)
    menos_home_loses = getStatsMatchsFile(2, 1, 2, df)
    menos_home_all = getStatsMatchsFile(2, 1, 0, df)
    menos_all_wins = getStatsMatchsFile(2, 0, 1, df)
    menos_all_loses = getStatsMatchsFile(2, 0, 2, df)
    all_away_wins = getStatsMatchsFile(0, 2, 1, df)
    all_away_loses = getStatsMatchsFile(0, 2, 2, df)
    all_away_all = getStatsMatchsFile(0, 2, 0, df)
    all_home_wins = getStatsMatchsFile(0, 1, 1, df)
    all_home_loses = getStatsMatchsFile(0, 1, 2, df)
    all_home_all = getStatsMatchsFile(0, 1, 0, df)
    all_all_wins = getStatsMatchsFile(0, 0, 1, df)
    all_all_loses = getStatsMatchsFile(0, 0, 2, df)

    # print(len(['mas_away_loses'] + list(mas_away_loses[0].values())))

    df_media = pd.DataFrame(
        columns=['Type', 'Num Matches', 'Points', 'FTM', 'FTA', 'FGM', 'FGA', '3PM', 'Asists', 'Turnovers', 'Steals', 'Blocks',
                 'Rebounds'])
    df_media.loc[0] = ['mas_away_wins'] + [mas_away_wins[2]] + list(mas_away_wins[0].values())
    df_media.loc[1] = ['mas_away_loses'] + [mas_away_loses[2]] + list(mas_away_loses[0].values())
    df_media.loc[2] = ['mas_away_all'] + [mas_away_all[2]] + list(mas_away_all[0].values())
    df_media.loc[3] = ['mas_home_wins'] + [mas_home_wins[2]] + list(mas_home_wins[0].values())
    df_media.loc[4] = ['mas_home_loses'] + [mas_home_loses[2]] + list(mas_home_loses[0].values())
    df_media.loc[5] = ['mas_home_all'] + [mas_home_all[2]] + list(mas_home_all[0].values())
    df_media.loc[6] = ['mas_all_wins'] + [mas_all_wins[2]] + list(mas_all_wins[0].values())
    df_media.loc[7] = ['mas_all_loses'] + [mas_all_loses[2]] + list(mas_all_loses[0].values())
    df_media.loc[8] = ['menos_away_wins'] + [menos_away_wins[2]] + list(menos_away_wins[0].values())
    df_media.loc[9] = ['menos_away_loses'] + [menos_away_loses[2]] + list(menos_away_loses[0].values())
    df_media.loc[10] = ['menos_away_all'] + [menos_away_all[2]] + list(menos_away_all[0].values())
    df_media.loc[11] = ['menos_home_wins'] + [menos_home_wins[2]] + list(menos_home_wins[0].values())
    df_media.loc[12] = ['menos_home_loses'] + [menos_home_loses[2]] + list(menos_home_loses[0].values())
    df_media.loc[13] = ['menos_home_all'] + [menos_home_all[2]] + list(menos_home_all[0].values())
    df_media.loc[14] = ['menos_all_wins'] + [menos_all_wins[2]] + list(menos_all_wins[0].values())
    df_media.loc[15] = ['menos_all_loses'] + [menos_all_loses[2]] + list(menos_all_loses[0].values())
    df_media.loc[16] = ['all_away_wins'] + [all_away_wins[2]] + list(all_away_wins[0].values())
    df_media.loc[17] = ['all_away_loses'] + [all_away_loses[2]] + list(all_away_loses[0].values())
    df_media.loc[18] = ['all_away_all'] + [all_away_all[2]] + list(all_away_all[0].values())
    df_media.loc[19] = ['all_home_wins'] + [all_home_wins[2]] + list(all_home_wins[0].values())
    df_media.loc[20] = ['all_home_loses'] + [all_home_loses[2]] + list(all_home_loses[0].values())
    df_media.loc[21] = ['all_home_all'] + [all_home_all[2]] + list(all_home_all[0].values())
    df_media.loc[22] = ['all_all_wins'] + [all_all_wins[2]] + list(all_all_wins[0].values())
    df_media.loc[23] = ['all_all_loses'] + [all_all_loses[2]] + list(all_all_loses[0].values())
    df_media.to_excel('media__' + fileName + '.xlsx')
    df_media.to_csv('media__' + fileName + '.csv')
    # print(df_media)

    df_desviacion = pd.DataFrame(
        columns=['Type', 'Num Matches', 'Points', 'FTM', 'FTA', 'FGM', 'FGA', '3PM', 'Asists', 'Turnovers', 'Steals', 'Blocks',
                 'Rebounds'])
    df_desviacion.loc[0] = ['mas_away_wins'] + [mas_away_wins[2]] + list(mas_away_wins[1].values())
    df_desviacion.loc[1] = ['mas_away_loses'] + [mas_away_loses[2]] + list(mas_away_loses[1].values())
    df_desviacion.loc[2] = ['mas_away_all'] + [mas_away_all[2]] + list(mas_away_all[1].values())
    df_desviacion.loc[3] = ['mas_home_wins'] + [mas_home_wins[2]] + list(mas_home_wins[1].values())
    df_desviacion.loc[4] = ['mas_home_loses'] + [mas_home_loses[2]] + list(mas_home_loses[1].values())
    df_desviacion.loc[5] = ['mas_home_all'] + [mas_home_all[2]] + list(mas_home_all[1].values())
    df_desviacion.loc[6] = ['mas_all_wins'] + [mas_all_wins[2]] + list(mas_all_wins[1].values())
    df_desviacion.loc[7] = ['mas_all_loses'] + [mas_all_loses[2]] + list(mas_all_loses[1].values())
    df_desviacion.loc[8] = ['menos_away_wins'] + [menos_away_wins[2]] + list(menos_away_wins[1].values())
    df_desviacion.loc[9] = ['menos_away_loses'] + [menos_away_loses[2]] + list(menos_away_loses[1].values())
    df_desviacion.loc[10] = ['menos_away_all'] + [menos_away_all[2]] + list(menos_away_all[1].values())
    df_desviacion.loc[11] = ['menos_home_wins'] + [menos_home_wins[2]] + list(menos_home_wins[1].values())
    df_desviacion.loc[12] = ['menos_home_loses'] + [menos_home_loses[2]] + list(menos_home_loses[1].values())
    df_desviacion.loc[13] = ['menos_home_all'] + [menos_home_all[2]] + list(menos_home_all[1].values())
    df_desviacion.loc[14] = ['menos_all_wins'] + [menos_all_wins[2]] + list(menos_all_wins[1].values())
    df_desviacion.loc[15] = ['menos_all_loses'] + [menos_all_loses[2]] + list(menos_all_loses[1].values())
    df_desviacion.loc[16] = ['all_away_wins'] + [all_away_wins[2]] + list(all_away_wins[1].values())
    df_desviacion.loc[17] = ['all_away_loses'] + [all_away_loses[2]] + list(all_away_loses[1].values())
    df_desviacion.loc[18] = ['all_away_all'] + [all_away_all[2]] + list(all_away_all[1].values())
    df_desviacion.loc[19] = ['all_home_wins'] + [all_home_wins[2]] + list(all_home_wins[1].values())
    df_desviacion.loc[20] = ['all_home_loses'] + [all_home_loses[2]] + list(all_home_loses[1].values())
    df_desviacion.loc[21] = ['all_home_all'] + [all_home_all[2]] + list(all_home_all[1].values())
    df_desviacion.loc[22] = ['all_all_wins'] + [all_all_wins[2]] + list(all_all_wins[1].values())
    df_desviacion.loc[23] = ['all_all_loses'] + [all_all_loses[2]] + list(all_all_loses[1].values())
    df_desviacion.to_excel('desviacion__' + fileName + '.xlsx')
    df_desviacion.to_csv('desviacion__' + fileName + '.csv')
    # print(df_desviacion)


df = pd.read_csv('NBAstats/generadores/matchsFile.csv')

df['dateStr'] = df['Day'].map(str) + '-' + df['Month'].map(str) + '-' + df['Year'].map(str)
df['date'] = pd.to_datetime(df[['Year', 'Month', 'Day']])
# a=df.date.unique()
# n = 816
# space_min = 30
# space_max = 150
# for i in range(n-space_min):
#     for j in range(i+space_min, min(n, space_max+i+1)):
#         # start_date = datetime.strptime(str(a[i]), '%d-%m-%Y')
#         # end_date = datetime.strptime(str(a[j]), '%d-%m-%Y')
#         start_date = datetime.datetime.utcfromtimestamp(a[i].tolist()/1e9)
#         end_date = datetime.datetime.utcfromtimestamp(a[j].tolist()/1e9)
#         print(start_date, end_date)
#         mask = (df['date'] > start_date) & (df['date'] < end_date)
#         ficheros(df[mask])
#         print(i,j)

########################    MES - DIA - AÑO           ##############################
sin = '2009'
to = '2010'
print(sin[2:] + '-' + to[2:])
start_date = '07-01-' + sin
end_date = '07-01-' + to
mask = (df['date'] > start_date) & (df['date'] < end_date)
ficheros(df[mask], '_' + sin[2:] + '-' + to[2:])

start_date = '07-01-' + sin
end_date = '01-01-' + to
mask = (df['date'] > start_date) & (df['date'] < end_date)
ficheros(df[mask], '1a-mitad__' + sin[2:] + '-' + to[2:])
start_date = '01-01-' + to
end_date = '07-01-' + to
mask = (df['date'] > start_date) & (df['date'] < end_date)
ficheros(df[mask], '2a-mitad__' + sin[2:] + '-' + to[2:])