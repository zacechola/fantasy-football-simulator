from random import normalvariate
from random import gauss
from numpy import array

MATCHUPS = 1000000

me_normal = array(
        [
        [23, 2.06],      #griffin
        [18, 1.14],     #foster
        [12, 3.41],     #mathews
        [21, 5.29],     #thomas
        [17, 4.05],     #cobb
        [12, 3.40],     #pettigrew
        [14, 2.73],     #johnson
        [12, 3.03],     #49ers
        [10, 2.72],      #hanson
        ]
        )

opp_normal = array(
        [
        [23, 3.08],     #brees
        [15, 2.93],     #johnson
        [16, 3.92],     #spiller
        [21, 5.80],     #green
        [13, 5.83],     #bowe
        [15, 6.56],     #witten
        [15, 5.35],     #graham
        [8, 1.83],      #ravens
        [8, 4.07]       #tucker
        ]
        )

me_range = [
        [23, 24],   #griffin
        [16,20],    #foster
        [5,18],     #mathews
        [12, 31],   #thomas
        [9, 24],    #cobb
        [6, 18],    #pettigrew
        [9, 19],    #johnson
        [7, 18],    #49ers
        [5, 15]     #hanson
        ]

opp_range = [
        [17, 29],   #brees
        [10, 20],   #johnson
        [9, 23],    #spiller
        [10, 31],   #green
        [2, 23],    #bowe
        [3, 27],    #witten
        [5, 25],    #graham
        [5, 11],    #ravens
        [1, 15]     #tucker
        ]

me_normal_points = 0
opp_normal_points = 0
me_normal_average = []
opp_normal_average = []
wins = 0
opp_win_average = []
opp_high_score = 0
me_high_score = 0

for x in range(0, MATCHUPS):
    for i in me_normal:
        mu = sum(i[:1])
        sigma = sum(i[1:])
        me_normal_points += gauss(mu, sigma)

    for j in opp_normal:
        mu = sum(i[:1])
        sigma = sum(i[1:])
        opp_normal_points += gauss(mu, sigma)


    if me_normal_points > opp_normal_points:
        wins += 1

    if me_normal_points < opp_normal_points:
        opp_win_average.append(opp_normal_points)

    if opp_normal_points > opp_high_score:
        opp_high_score = opp_normal_points

    if me_normal_points > me_high_score:
        me_high_score = me_normal_points


    me_normal_average.append(me_normal_points)
    opp_normal_average.append(opp_normal_points)
    
    # reset vars
    me_normal_points = 0
    opp_normal_points = 0


print "Wins: %d / %d" % (wins, MATCHUPS)

print 'Me Normal Average:'
print sum(me_normal_average) / float(len(me_normal_average))

print 'Opponent Normal Average:'
print sum(opp_normal_average) / float(len(opp_normal_average))

print 'Opponent Wins Average Scores:'
print sum(opp_win_average) / float(len(opp_win_average))

print 'Opponent High Score:'
print opp_high_score

print 'Me High Score:'
print me_high_score
