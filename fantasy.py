import argparse
from random import normalvariate
from sys import exit
from numpy import array

parser = argparse.ArgumentParser(description='Calculate fantasy football win probability', 
        epilog='And that is how you win your league')
parser.add_argument("matchups", help="the number of matchup trials to run", type=int)
parser.add_argument("-s", "--spread", help="calculate the chance you exceeding a spread", type=int)
parser.add_argument("-q", "--quiet", help="do not print matchups", action="store_true")
parser.parse_args()
args = parser.parse_args()

MATCHUPS = args.matchups

if MATCHUPS < 6000:
    print "Run at least 6000 matchups to avoid errors!"
    exit()


# make bets and win money
if args.spread:
    spread_baseline = args.spread
else:
    spread_baseline = 0

#spread_baseline = int(raw_input("Enter a winning points spread: "))

me = array(
        [
        [24, 3.83],     #griffin
        [18.10, 1.69],  #foster
        [13.80, 2.64],  #mathews
        [13, 0],        #thomas
        [17.98, 3.67],  #cobb
        [12.25, 2.50],  #pettigrew
        [16.03, 3.14],  #johnson
        [11.15, 3.03],  #49ers
        [10.03, 3.13],  #hanson
        ]
        )


opp = array(
        [
        [22.53, 3.27],  #brees
        [15.88, 2.84],  #johnson
        [16.53, 2.86],  #spiller
        [20.20, 6.16],  #green
        [12., 4.79],    #bowe
        [15.70, 6.22],  #witten
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
me_average_win_spread = []
opp_average_win_spread = []


def spread_freq(baseline):
    count = 0
    for q in me_average_win_spread:
        if q > baseline:
            count += 1
    return count

def score_freq(llimit, ulimit, team):
    count = 0
    def test(team):
        if team == 'opp':
            return opp_normal_average
        if team == 'me':
            return me_normal_average

    for q in test(team):
        if q <= ulimit and q >= llimit:
            count += 1
    return count

def score(data):
    points = 0
    for i in data:
        mu = sum(i[:1])
        sigma = sum(i[1:])
        score = int(normalvariate(mu, sigma)) # ESPN league is whole numbers
        points += score
    return points



def freq_table():
    bounds = array( 
            [
                [80.5, 90.5],
                [90.5, 99.5],
                [99.5, 110.5],
                [110.5, 120.5],
                [120.5, 130.5],
                [130.5, 140.5],
                [140.5, 150.5],
                [150.5, 160.5],
                [160.5, 170.5],
                [170.5, 180.5],
                [180.5, 190.5]
                ]
                )

    for i in bounds:
        upper = i[:1]
        lower = i[1:]
        print "%d.5 - %d.5 => %d \t\t %d.5 - %d.5 => %d " % (upper, lower, score_freq(upper, lower, 'me'), upper, lower, score_freq(upper, lower, 'opp'))


for i in range(0, int(MATCHUPS)):
    me_score = score(me)
    opp_score = score(opp)
    opp_normal_average.append(opp_score)
    me_normal_average.append(me_score)
    
    if not args.quiet:
        print "Me:  %d" % me_score
        print "Opp: %d" % opp_score
        print "---"

    #count wins
    if me_score > opp_score:
        wins += 1
        me_win_average.append(me_score)
        me_average_win_spread.append(me_score - opp_score)

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
        opp_average_win_spread.append(opp_score - me_score)

    #find ties
    if opp_score == me_score:
        ties += 1

#output
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
print "Average opponent winning spread:"
opp_win_spread = float(sum(opp_average_win_spread)) / float(len(opp_average_win_spread))
print opp_win_spread
print "Ties %:"
print float((ties) / float(MATCHUPS)) * 100

print ""# make bets and win money

print "My winning score average:"
me_win_score_average = float(sum(me_win_average)) / float(len(me_win_average))
print me_win_score_average
print "My average winning spread:"
me_win_spread = float(sum(me_average_win_spread)) / float(len(me_average_win_spread))
print me_win_spread

print ""
print "My win spread percent over %d points" % spread_baseline
print (spread_freq(spread_baseline) / float(MATCHUPS)) * 100

print ""

freq_table()

print "----\n"
