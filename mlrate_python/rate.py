#!/usr/bin/python

import math
import random
from datetime import datetime, timedelta

#MLRATE_K = 0.85               # kgs3 30k-5k
MLRATE_K = 1.30              # kgs3 2d+
#HALF_LIFE = timedelta(days=15)
HALF_LIFE = timedelta(days=45)
CUTOFF = timedelta(days=180)

RATING_MIN = -99.0
RATING_MAX = 99.0
CLOSE_ENOUGH = 0.0005        # Terminate inner (bisection) loop when we're this close
CHANGE_LIMIT = 0.001         # Terminate outer loop when no one's rating changes more than this
GLOBAL_TURNS_MAX = 1000      # saftey, don't run more than this
#GLOBAL_TURNS_MAX = 1        # test with just 1 outer loop

MLRATE_S = 1/math.exp(MLRATE_K)
HALF_LIFE_IN_SECONDS = HALF_LIFE.seconds + HALF_LIFE.days*3600*24
NOW    = datetime.now()


class PlayerInfo:
   name = ""
   def __init__(self, name, rating):
      self.name = name
      self.rating = rating
      self.anchor = False
      self.trueStrength = rating
   def printme(self):
      return "%s %0.2f" % (self.name, self.rating)

class GameInfo:
   def __init__(self, date, whitePlayer, blackPlayer, handicap, komi, whiteWin):
      self.date        = date
      self.whitePlayer = whitePlayer
      self.blackPlayer = blackPlayer
      self.handicap    = handicap
      self.komi        = komi
      self.whiteWin    = whiteWin
   def printme(self):
      if (self.whiteWin):
         return "+" + self.whitePlayer.name + " vs " + self.blackPlayer.name
      else:
         return self.whitePlayer.name + " vs " + "+" + self.blackPlayer.name

def weight(game):
   age = NOW - game.date
   if (age > CUTOFF):
      return 0  # games past cutoff have no effect
   age_in_seconds = float(age.seconds + age.days*3600*24)
   tmpWeight = math.pow(0.5, age_in_seconds/HALF_LIFE_IN_SECONDS)
   return tmpWeight

def pWin(diff):
  return 1/(1+math.pow(MLRATE_S,diff))

def diffGivenPWin(pW):
  return math.log( ((1-pW)/pW)) / MLRATE_K

def mlrate():
   globturns = 0   # Counts the turns of the outer loop.

   # Assign initial ratings  (NA)
   # Remove players with no wins or no losses (Not done yet)

   #Outer loop
   outerDone = False
   while (not outerDone):
      maxp = 0
      maxchange = 0
      globturns = globturns + 1
      outerDone = True
      # Loop over all players
      for playerName, currPlayer in players.iteritems():
         if (currPlayer.anchor==True):
            continue
         ileft  = RATING_MIN
         iright = RATING_MAX
         nwin   = 0
         nloss  = 0
         bestwin  = RATING_MIN
         worstloss = RATING_MAX
         #outputArea.append(String.valueOf("working on " + currPlayer + "\n"))
         curr_guess = prev_guess = currPlayer.rating

         bisectionDone = False
         while (not bisectionDone):
            sum = 0
            for currGame in games:
              if (currGame.whitePlayer == currPlayer):
                oppPlayer = currGame.blackPlayer
                currPlayerWon = currGame.whiteWin
                currPlayerGameAdvantage = -currGame.handicap  # handicap favored opponent
              elif (currGame.blackPlayer == currPlayer):
                oppPlayer = currGame.whitePlayer
                currPlayerWon = not currGame.whiteWin
                currPlayerGameAdvantage = currGame.handicap   # handicap favored currPlayer
              else:
                continue  # current player not involved in this game
              currPlayerOverallAdvantage = curr_guess - oppPlayer.rating + currPlayerGameAdvantage

              add = (pWin(currPlayerOverallAdvantage) - currPlayerWon) * weight(currGame)
              sum = sum + add
              if currPlayerWon:
                nwin += 1
                bestwin = max(bestwin, oppPlayer.rating - currPlayerGameAdvantage)
              else:
                nloss += 1
                worstloss = min(worstloss, oppPlayer.rating - currPlayerGameAdvantage)

              #print "  %s %s" % (curr_guess, add)

              #System.out.println(
              #    "  currPlayer = " + currPlayer + "\n" +
              #    "  currGame   = " + currGame + "\n" +
              #    "  oppPlayer  = " + oppPlayer + "\n" +
              #    "  GameAd     = " + currPlayerGameAdvantage + "\n" +
              #    "  TotAd      = " + currPlayerOverallAdvantage + "\n" +
              #    "  add        = " + add + "\n" +
              #    "  sum        = " + sum + "\n"
              #)

            # end for games
            if sum > 0:
               iright = curr_guess  # Root is somewhere to the left
            else:
               ileft = curr_guess   # Root is somewhere to the right
            curr_guess = (iright + ileft) / 2
            bisectionDone = iright - ileft < CLOSE_ENOUGH   # done when we're close enough
            # handle no wins/losses cases
            if nloss == 0:
               curr_guess = bestwin + 1
               bisectionDone = True
            if nwin == 0:
               curr_guess = worstloss - 1
               bisectionDone = True
         # end while
         if ( math.fabs(curr_guess - currPlayer.rating) > maxchange ):
            maxchange = math.fabs(curr_guess - currPlayer.rating)
         currPlayer.rating = curr_guess
         #print "update: " + currPlayer.printme()
         # circular_check not implemented
      # end for players
      outerDone = (maxchange < CHANGE_LIMIT) or (globturns >= GLOBAL_TURNS_MAX)
   # end outer loop
# end mlrate function

def printPlayers():
   print "players"
   for k, v in players.iteritems():
      print v.printme()
   print

def printGames():
  print "games"
  for g in games:
     print "%s daysold=%s H=%s W=%s" %(g.printme(), (NOW-g.date).days, g.handicap, weight(g))
  print

def initPlayers():
   players.clear()
   players["yoyoma"] = PlayerInfo("yoyoma", 0.0)
   players["killrducky"] = PlayerInfo("killrducky", 0.0)
   players["killrducky"].anchor = True

def winstreakTest():
   for days in range (CUTOFF.days/2):
      games.append(GameInfo(NOW-timedelta(days=days*2), players["yoyoma"], players["killrducky"], 0, 6.5, True))
      games.append(GameInfo(NOW-timedelta(days=days*2), players["yoyoma"], players["killrducky"], 0, 6.5, False))
   printPlayers()
   printGames()
   mlrate()
   printPlayers()
   for winstreak in range(30):
      games.append(GameInfo(NOW, players["yoyoma"], players["killrducky"], 0, 6.5, True))
      mlrate()
      print "%d %d %s" % (winstreak+1, len(games), players["yoyoma"].printme())

def pickHandicap(white, black):
   diff = white.rating - black.rating
   handicap = math.floor(diff + 0.5)
   # games are always underhandicapped by half a stone
   if handicap > 0.5:
      handicap -= 0.5
   elif handicap < -0.5:
      handicap += 0.5
   #print "pick", white.rating, black.rating, handicap
   return handicap
   
   

def randomNewPlayerTest():
   histogram = []
   for tests in range(1000):
      initPlayers()
      del games[:]
      players["yoyoma"].trueStrength = 2
      ratingHistory = []
      for numgames in range (10):
         handicap = pickHandicap(players["yoyoma"], players["killrducky"])
         trueProbWin = pWin(players["yoyoma"].trueStrength - players["killrducky"].trueStrength - handicap)
         win = random.random() < trueProbWin
         games.append(GameInfo(NOW, players["yoyoma"], players["killrducky"], handicap, 6.5, win))
         mlrate()
         #print handicap, trueProbWin, "%", win, players["yoyoma"].printme()
         #ratingHistory.append("%s%0.2f" %(("L", "W")[win], players["yoyoma"].rating))
         ratingHistory.append(players["yoyoma"].rating)
      #printGames()
      #printPlayers()
      #fig = plt.figure()
      #ax = fig.add_subplot(111)
      #ax.plot(ratingHistory)
      #plt.show()
      histogram.append(players["yoyoma"].rating)
   #plt.show()
   if True:
      fig = plt.figure()
      ax = fig.add_subplot(111)
      #n, bins, patches = ax.hist(histogram, 20, normed=1, facecolor="green", alpha=0.75)
      n, bins, patches = ax.hist(histogram, 20)
      print n, bins
      bincenters = 0.5*(bins[1:]+bins[:-1])
      plt.show()
   



players = {}
games   = []
initPlayers()
winstreakTest()
#randomNewPlayerTest()


#print "pWin(%f)=%f" % (players["yoyoma"].rating, pWin(players["yoyoma"].rating))
#print "diff=%f" % diffGivenPWin(2.0/3.0)



