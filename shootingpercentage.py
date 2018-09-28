import requests
import json
from math import sqrt
from math import floor
from math import ceil

#The starting year of the season (by default this is the 2017-2018 season).
#The earliest year that will work is 2010.
YEAR = "2017"

#Constants for the type of games played
PRESEASON = "01"
REGULARSEASON = "02"
PLAYOFFS = "03"
ALLSTAR = "04"

goals = []
nongoals = []

def distance(x,y):
   return (sqrt((89-x)**2+(y)**2))

#Loop through every game in a season (1271 for 31 teams)
for i in range(1,1272):
   print (str(int(ceil(i/12.72))))
   try:
      #Get the API url
      url = "https://statsapi.web.nhl.com/api/v1/game/" + YEAR + REGULARSEASON + str("%04d" %(i,)) + "/feed/live"
      response = requests.get(url)
      for j in range(1000):
         try:
            if response.json()["liveData"]["plays"]["allPlays"][j]["result"]["event"] == "Goal":
               goalx = abs(float(response.json()["liveData"]["plays"]["allPlays"][j]["coordinates"]["x"]))
               goaly = abs(float(response.json()["liveData"]["plays"]["allPlays"][j]["coordinates"]["y"]))
               goals.append((goalx,goaly,distance(goalx,goaly)))
            if response.json()["liveData"]["plays"]["allPlays"][j]["result"]["event"] == "Shot":
               nongoalx = abs(float(response.json()["liveData"]["plays"]["allPlays"][j]["coordinates"]["x"]))
               nongoaly = abs(float(response.json()["liveData"]["plays"]["allPlays"][j]["coordinates"]["y"]))
               nongoals.append((nongoalx,nongoaly,distance(nongoalx,nongoaly)))
         except IndexError:
            break
   except KeyError:
      continue

shotCounter = [0 for i in range(100)]
goalCounter = [0 for i in range(100)]

for i in range(len(goals)):
   goalCounter[int(floor(goals[i][2]))] = goalCounter[int(floor(goals[i][2]))] + 1
for i in range(len(nongoals)):
   shotCounter[int(floor(nongoals[i][2]))] = shotCounter[int(floor(nongoals[i][2]))] + 1

print 'Distance(ft)\tShooting Percentage\n'
for i in range(len(goalCounter)):
   if goalCounter[i] + shotCounter[i] != 0:
      print str(i+1) + '\t\t' + str(goalCounter[i]) + '/' + str(goalCounter[i]+shotCounter[i]) + ' = ' + \
         str(float(goalCounter[i])/float((goalCounter[i]+shotCounter[i])))
