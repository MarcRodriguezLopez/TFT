from generadores import match_list
from generadores import GetLists
from generadores import teams_list
from generadores import fouls_generator
from generadores import points_and_assists_generator
from generadores import rest_generator
from generadores import steals_blocks_rebounds_generator
from generadores import substitutions_generator
from generadores import turnovers_generator
from generadores import refill_match
import pandas as pd

inputFile = 'playbyplay20052010.txt'

teamsFile = 'teamsFile.csv'
listsFile = 'listsFile.csv'
matchsFile = inputFile + 'matchsFile.csv'
foulsFile = inputFile + 'foulsFile.csv'
pointsFile = inputFile + 'pointsFile.csv'
assistsFile = inputFile + 'assistsFile.csv'
restFile = inputFile + 'restFile.csv'
stealsBlocksReboundsFile = inputFile + 'stealsBlocksReboundsFile.csv'
substitutionsFile = inputFile + 'substitutionsFile.csv'
turnoversFile = inputFile + 'turnoversFile.csv'
lolFile = 'lol.csv'

#teams_list.main(inputFile, teamsFile)
print('teams list completed')
#GetLists.main(inputFile, listsFile)
print('lists completed')
#match_list.main(inputFile, matchsFile, teamsFile)
print('match list completed')
# fouls_generator.main(inputFile, foulsFile, teamsFile, listsFile, matchsFile)
print('fouls file completed')
# points_and_assists_generator.main(inputFile, pointsFile, lolFile, assistsFile, teamsFile, listsFile, matchsFile)
print('points and assists completed')
rest_generator.main(inputFile, restFile, teamsFile, listsFile, matchsFile)
print('rest completed')
#steals_blocks_rebounds_generator.main(inputFile, stealsBlocksReboundsFile, teamsFile, matchsFile)
print('SBR completed')
#substitutions_generator.main(inputFile, substitutionsFile, teamsFile, matchsFile)
print('substitutions completed')
#turnovers_generator.main(inputFile, turnoversFile, teamsFile, listsFile, matchsFile)
print('turnovers completed')
# refill_match.main(matchsFile, foulsFile, pointsFile, assistsFile, turnoversFile, stealsBlocksReboundsFile, listsFile)
print('all completed')