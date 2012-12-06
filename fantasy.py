from random import normalvariate
from numpy import *
from sys import exit

MATCHUPS = int(raw_input("How many matchups to run? "))

if MATCHUPS < 6000:
    print "Run at least 6000 matchups to avoid divide by zero errors!"
    MATCHUPS = int(raw_input("How many matchups to run? "))

me = array(
        [
        [20.75, 2.06],  #griffin
        [17.35, 1.14],  #foster
        [14.55, 3.41],  #mathews
        [24., 5.29],    #thomas
        [18.23, 4.05],  #cobb
        [13.25, 3.40],  #pettigrew
        [15.78, 2.73],  #johnson
        [11.15, 3.03],  #49ers
        [9.78, 2.72],   #hanson
        ]
        )

opp = array(
        [
        [20.53, 3.08],  #brees
        [16.63, 2.93],  #johnson
        [17.28, 3.92],  #spiller
        [19.95, 5.80],  #green
        [5.33, 6.25],   #shorts*
        [15.95, 6.56],  #witten
        [16., 5.35],    #graham
        [3.55, 1.83],   #ravens
        [6., 4.07]      #tucker
        ]
        )

me_normal_average = []
opp_normal_average = []
wins = 0
opp_win_average = []
me_win_average = []
opp_high_score = 0
me_high_score = 0
ties = 0
opp_low_score = 900
me_low_score = 900

def score(data):
    points = 0
    for i in data:
        mu = sum(i[:1])
        sigma = sum(i[1:])
        score = int(normalvariate(mu, sigma))
        points += score
    return points

for i in range(0, MATCHUPS):
    me_score = score(me)
    opp_score = score(opp)
    opp_normal_average.append(opp_score)
    me_normal_average.append(me_score)

    print "Me:  %d" % me_score
    print "Opp: %d" % opp_score
    print "---"

    #count wins
    if me_score > opp_score:
        wins += 1
        me_win_average.append(me_score)

    #find high score
    if me_score > me_high_score:
        me_high_score = me_score

    #find opponent high score
    if opp_score > opp_high_score:
        opp_high_score = opp_score

    #find low score
    if me_score < me_low_score:
        me_low_score = me_score

    if opp_score < opp_low_score:
        opp_low_score = opp_score

    #find losses
    if opp_score >= me_score:
        opp_win_average.append(opp_score)

    #find ties
    if opp_score == me_score:
        ties += 1


print "\n----"
print "Win %:"
print (float(wins) / float(MATCHUPS)) * 100
print ""
print "My average:"
print float(sum(me_normal_average)) / float(len(me_normal_average))
print "Opponent average:"
print float(sum(opp_normal_average)) / float(len(opp_normal_average))
print ""
print "My highest score:"
print me_high_score
print "My lowest score:"
print me_low_score
print ""
print "Opponent highest score:"
print opp_high_score
print "Opponent low score:"
print opp_low_score
print ""
print "Opponent winning score average:"
opp_win_score_average = float(sum(opp_win_average)) / float(len(opp_win_average))
print opp_win_score_average
print "My winning score average:"
me_win_score_average = float(sum(me_win_average)) / float(len(me_win_average))
print me_win_score_average
print ""
print "Ties %:"
print float((ties) / float(MATCHUPS)) * 100
print "----\n"
