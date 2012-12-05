from random import normalvariate
from random import gauss
from numpy import array

MATCHUPS = 50000

me = array(
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

opp = array(
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

me_normal_average = []
opp_normal_average = []
wins = 0
opp_win_average = []
opp_high_score = 0
me_high_score = 0

def score(data):
    points = 0
    for i in data:
        mu = sum(i[:1])
        sigma = sum(i[1:])
        score = gauss(mu, sigma)
        points += score
    return points

for x in range(0, MATCHUPS):
    me_score = score(me)
    opp_score = score(opp)
    opp_normal_average.append(opp_score)
    me_normal_average.append(me_score)

    if me_score > opp_score:
        wins += 1

    if me_score > me_high_score:
        me_high_score = me_score

    if opp_score > opp_high_score:
        opp_high_score = opp_score

print "Win %:"
print (float(wins) / float(MATCHUPS)) * 100

print "My average:"
print float(sum(me_normal_average)) / float(len(me_normal_average))
print "Opponent average:"
print float(sum(opp_normal_average)) / float(len(opp_normal_average))

print "My highest score:"
print me_high_score

print "Opponent highest score:"
print opp_high_score

