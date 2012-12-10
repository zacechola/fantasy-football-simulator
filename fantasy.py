import argparse, csv
from random import normalvariate
from numpy import array
from scipy import stats

# Parse arguments from the command line

parser = argparse.ArgumentParser(description='Calculate fantasy football win probability', 
        epilog='And that is how you win your league')
parser.add_argument("matchups", help="the number of matchup trials to run", type=int)
parser.add_argument("opp_file", help="opponent file to open")
parser.add_argument("-s", "--spread", help="calculate the chance your score exceeds a spread", type=int)
parser.add_argument("-q", "--quiet", help="do not print matchups", action="store_true")
parser.add_argument("-t", "--ties", help="count ties as wins", action="store_true")
parser.parse_args()
args = parser.parse_args()


# Initialize some variables

me_file = open('teams/me.csv')
opp_file = open(args.opp_file)

MATCHUPS = args.matchups

if MATCHUPS < 6000:
    print "Run at least 6000 matchups to avoid errors!"
    MATCHUPS = int(raw_input("Enter a number of matchup trials: "))

# make bets and win money
if args.spread:
    spread_baseline = args.spread

if args.quiet:
    print "Running %d trials..." % MATCHUPS

# Generates multidimensional list of team stats

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
    return team_stats



# Calculate the frequency of scores over a threshold
# Returns a count

def spread_freq(baseline):
    count = 0
    for q in me_average_win_spread:
        if q > baseline:
            count += 1
    return count

# Calculate the frequency of scores within defined bounds
# Returns counts

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

# Generate player scores based on data in array and sum the points
# Returns total points

def score(data):
    points = 0
    for i in data:
        mu = sum(i[:1])
        sigma = sum(i[1:])
        score = int(normalvariate(mu, sigma)) # ESPN league is whole numbers
        points += score
    return points

# Implements score_freq
# Defines the bounds for the frequency table
# prints the output

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
        print "%d.5 - %d.5 => %d \t\t %d.5 - %d.5 => %d " % (
                upper, lower, score_freq(upper, lower, 'me'), 
                upper, lower, score_freq(upper, lower, 'opp'))



me = array(generate_team_stats(me_file))
opp = array(generate_team_stats(opp_file))
me_normal_average = []
opp_normal_average = []
me_average_win_spread = []
opp_average_win_spread = []
opp_win_average = []
me_win_average = []

wins = 0
opp_high_score = 0
me_high_score = 0
ties = 0

# this is a hack, scores should never be this high
opp_low_score = 900
me_low_score = 900



# Main loop

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
        if args.ties:
            wins += 1
            me_average_win_spread.append(me_score - opp_score)


# Output
print "\n----"
wins_percentage = float((wins) / float(MATCHUPS)) * 100
ties_percentage = float((ties) / float(MATCHUPS)) * 100

if args.ties:
    print "Win: {}% \n".format(wins_percentage)
else:
    print "Win: {}%".format(wins_percentage)
    print "Tie: {}% \n".format(ties_percentage)




if args.spread:
    spread_percent = (spread_freq(spread_baseline) / float(MATCHUPS)) * 100
    if spread_percent > 50.00:
        print "Wins over {} points: {}%".format(spread_baseline, spread_percent)
        print "You have a positive expected value on an even money spread bet! \n"
    else:
        print "Wins over {} points: {}% \n".format(spread_baseline, spread_percent)


print "My average: {}".format(float(sum(me_normal_average)) / float(len(me_normal_average)))
print "Opponent average: {} \n".format(float(sum(opp_normal_average)) / float(len(opp_normal_average)))

print "My highest score: %d" % me_high_score
print "My lowest score: %d" % me_low_score
print "My space: %d \n" % (me_high_score - me_low_score)

print "Opponent highest score: %d" % opp_high_score
print "Opponent low score: %d" % opp_low_score
print "Opponent space: %d \n" % (opp_high_score - opp_low_score)

if opp_win_average:
    opp_win_score_average = float(sum(opp_win_average)) / float(len(opp_win_average))
    print "Opponent winning score average: %f" % opp_win_score_average
    opp_win_spread = float(sum(opp_average_win_spread)) / float(len(opp_average_win_spread))
    print "Opponent average winning spread: %f \n" % opp_win_spread

if me_win_average:
    me_win_score_average = float(sum(me_win_average)) / float(len(me_win_average))
    print "My winning score average: %f" % me_win_score_average
    me_win_spread = float(sum(me_average_win_spread)) / float(len(me_average_win_spread))
    print "My average winning spread: %f \n" % me_win_spread

print "Frequency of scores:"
print "me \t \t \t \t opp"
freq_table()

print "----\n"
