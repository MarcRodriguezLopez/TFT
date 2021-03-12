import pandas as pd


def getOverTime(id, foulsFile):
    df = pd.read_csv(foulsFile)
    for x in range(len(df)):
        if "-" in df["Time"][x] and id == df["Code"][x]:
            return 1
    return 0


def getPoints(id, away, home, pointsFile, freeThrowId):  # return [Points, FTM, FTA, FGM, FGA, 3PM]
    df = pd.read_csv(pointsFile)
    resL = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for x in range(len(df)):
        if id == df["Code"][x]:
            if 1 == df["MissOrMade"][x]:
                if away == df["Team"][x]:
                    resL[0] += df["Value"][x]
                    if df["Value"][x] == 1:
                        resL[2] += 1
                        resL[4] += 1
                    elif df["Value"][x] == 2:
                        resL[6] += 1
                        resL[8] += 1
                    else:
                        resL[10] += 1
                elif home == df["Team"][x]:
                    resL[1] += df["Value"][x]
                    if df["Value"][x] == 1:
                        resL[3] += 1
                        resL[5] += 1
                    elif df["Value"][x] == 2:
                        resL[7] += 1
                        resL[9] += 1
                    else:
                        resL[11] += 1
            else:
                if away == df["Team"][x]:
                    if str(df["TypeShot"][x]) == str(freeThrowId):
                        resL[4] += 1
                    else:
                        resL[8] += 1
                elif home == df["Team"][x]:
                    if str(df["TypeShot"][x]) == str(freeThrowId):
                        resL[5] += 1
                    else:
                        resL[9] += 1
    return resL


def getAssists(id, away, home, assistsFile):  # return [away assists, home assists]
    df = pd.read_csv(assistsFile)
    awayAssists = 0
    homeAssists = 0
    for x in range(len(df)):
        if id == df["Code"][x]:
            if away == df["Team"][x]:
                awayAssists += 1
            elif home == df["Team"][x]:
                homeAssists += 1
    resA = []
    resA.insert(len(resA), awayAssists)
    resA.insert(len(resA), homeAssists)
    return resA


def getTurnovers(id, away, home, turnoversFile):  # return [away assists, home assists]
    df = pd.read_csv(turnoversFile)
    awayTurnovers = 0
    homeTurnovers = 0
    for x in range(len(df)):
        if id == df["Code"][x]:
            if away == df["Team"][x]:
                awayTurnovers += 1
            elif home == df["Team"][x]:
                homeTurnovers += 1
    resA = []
    resA.insert(len(resA), awayTurnovers)
    resA.insert(len(resA), homeTurnovers)
    return resA


def getSBR(id, away, home, sbrFile):  # return [away steals, away blocks, away rebounds, home steals, home blocks, home rebounds]
    df = pd.read_csv(sbrFile)
    resA = [0, 0, 0, 0, 0, 0]
    for x in range(len(df)):
        if id == df["Code"][x]:
            if 1 == df["Steal"][x]:
                if away == df["Team"][x]:
                    resA[0] += 1
                elif home == df["Team"][x]:
                    resA[1] += 1
            elif 1 == df["Block"][x]:
                if away == df["Team"][x]:
                    resA[2] += 1
                elif home == df["Team"][x]:
                    resA[3] += 1
            elif 1 == df["Rebound"][x]:
                if away == df["Team"][x]:
                    resA[4] += 1
                elif home == df["Team"][x]:
                    resA[5] += 1
    return resA


def main(inOutFile, foulsFile, pointsFile, assistsFile, turnoversFile, sbrFile, listsFile):
    freeThrowId = 0
    df = pd.read_csv(listsFile)
    for i in range(len(df)):
        action = df["Action"][i]
        id = df["Id"][i]
        type = df["Type"][i]
        if action == "Free Throw":
            freeThrowId = id
    df = pd.read_csv(inOutFile)
    for x in range(3):
        i = x + 6130
        vis = df["Away"][i]
        loc = df["Home"][i]
        #df["OverTime"][i] = getOverTime(i, foulsFile)
        a = getPoints(i, vis, loc, pointsFile, freeThrowId)
        df["AwayPoints"][i] = a[0]
        df["HomePoints"][i] = a[1]
        df["AwayFTM"][i] = a[2]
        df["HomeFTM"][i] = a[3]
        df["AwayFTA"][i] = a[4]
        df["HomeFTA"][i] = a[5]
        df["AwayFGM"][i] = a[6]
        df["HomeFGM"][i] = a[7]
        df["AwayFGA"][i] = a[8]
        df["HomeFGA"][i] = a[9]
        df["Away3PM"][i] = a[10]
        df["Home3PM"][i] = a[11]
        a = getAssists(i, vis, loc, assistsFile)
        df["AwayAssists"][i] = a[0]
        df["HomeAssists"][i] = a[1]
        # a = getTurnovers(i, vis, loc, turnoversFile)
        # df["AwayTurnovers"][i] = a[0]
        # df["HomeTurnovers"][i] = a[1]
        # a = getSBR(i, vis, loc, sbrFile)
        # df["AwaySteals"][i] = a[0]
        # df["HomeSteals"][i] = a[1]
        # df["AwayBlocks"][i] = a[2]
        # df["HomeBlocks"][i] = a[3]
        # df["AwayRebounds"][i] = a[4]
        # df["HomeRebounds"][i] = a[5]
        print("match {} completed".format(i))
    df.to_csv(inOutFile, index=False)