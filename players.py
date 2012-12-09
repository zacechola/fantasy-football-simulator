import csv
from scipy import stats
from numpy import array
from random import normalvariate


teamfile = open('teams/a.csv')

def generate_team_stats(csv_file):
    data = csv.reader(csv_file)
    rownum = 0
    player_stats = []
    team_stats = []
    for row in data:
        predictions = []

        if rownum == 0:
            header = row
        else:
            colnum = 0
            for col in row:
                if colnum == 0:
                    player = col
                if colnum != 0:
                    predictions.append(float(col))
                
                colnum += 1
            
            
            mean = array(predictions).mean()
            std = array(predictions).std()
            player_stats = [mean, std]
            team_stats.append(player_stats)

        rownum += 1
    print team_stats
    return team_stats

generate_team_stats(teamfile)
teamfile.close()
