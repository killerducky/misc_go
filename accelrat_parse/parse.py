#!/usr/bin/env python2.6

import re
import sys
import os

class Player:
   def __init__(self, agaid, name, rating):
      self.agaid  = int(agaid)
      self.name   = name
      self.rating = float(rating)
      self.round  = []

class Game:
   def __init__(self, white, black, winner, handicap, komi):
      self.white = players_byaga[white]
      self.black = players_byaga[black]
      self.winner = winner
      self.handicap = int(handicap)
      self.komi = int(komi)
   def my_opp(self, me):
      if self.white == me: return self.black 
      else:                return self.white
   def handi_advantage(self):
      if self.handicap == 0:
         if   self.komi ==  5: handi_advantage = 0.0
         elif self.komi ==  0: handi_advantage = 0.5
         elif self.komi == -5: handi_advantage = 1.0
         else: sys.exit("invalid self.komi:" + str(self.komi))
      else:
         handi_advantage = self.handicap - 0.5
      return handi_advantage
   def rating_advantage(self):
      if (self.white.rating * self.black.rating) < 0 : 
         return self.white.rating - self.black.rating - 2   # compensate for dan/kyu border
      else:
         return self.white.rating - self.black.rating
   def my_result(self, me):
      if self.white == me: return winner=="W"
      else:                return winner=="B"
   def white_advantage(self):
      return self.rating_advantage() - self.handi_advantage()
   def my_advantage(self, me):
      if self.white == me: return self.white_advantage()
      else:                return -self.white_advantage()

players_byaga = {}

f = open("register.tde")
for line in f:
   line = line.rstrip()                # strip trailing whitespace including newline
   line = re.sub("#.*", "", line)      # strip comments
   if len(line) == 0: continue         # if nothing left, continue
   m = line.split("\t")                
   agaid, name, rating = m[:3]
   #print agaid, name, rating
   players_byaga[agaid] = Player(agaid, name, rating)
f.close

f = open("TRUERATS.tde")
for line in f:
   m = re.split("\s+|=", line)
   #print m
   agaid = m[0]
   truerating = m[2]
   players_byaga[agaid].truerating = truerating
f.close

round = 1
while (os.path.exists(str(round)+".tde")):
   f = open(str(round)+".tde")
   for line in f:
      line = line.rstrip()
      line = re.sub("##.*", "", line)
      if len(line) == 0: continue
      m = re.split("\s*[#:]\s*", line)
      tmp = m[0]
      white, black, winner, handicap, komi = re.split("\s+", tmp)
      game = Game(white, black, winner, handicap, komi)
      players_byaga[white].round.append(game)
      players_byaga[black].round.append(game)
   f.close
   round += 1


def tdwrap(td):
   return "<td>" + str(td) + "</td>"

print "<table border=\"1\">"
print "<tr><td>agaid</td><td>name</td><td>rating</td>",
for x in range(1, round): print tdwrap(x)    
print "</tr>"
#print tdwrap(x) for x in range(1, round)     # why can't I do a comprehension here?
for player in players_byaga.values():
   #for tmp in [player.agaid, player.name, player.rating, player.truerating]: print tdwrap(tmp)
   print tdwrap(player.agaid), tdwrap(player.name)
   print tdwrap("enter " + str(player.rating) + "<br>" + "true " + str(player.truerating))
   for game in player.round:
      print "<td>",
      print game.my_opp(player).name, "<br>",
      print "my_curr_rating", "<br>",
      print "opp_rating", game.my_opp(player).rating, "<br>",
      print "win?", game.my_result(player), "<br>",
      print "handi", "%0.2f" % (game.handi_advantage()), "<br>",
      print "rat_diff", "%0.2f" % (game.rating_advantage()), "<br>",
      print "my_adv", "%0.2f" %(game.my_advantage(player)), "<br>",
      print "</td>"
      #if player.agaid == 9771 and game.my_opp(player).agaid == 4408:
      #   print "<td>", player.rating, game.my_opp(player).rating, "<td>"
   print
   print "</tr>"
print "</table>"
