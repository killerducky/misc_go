#!/usr/bin/env python2.6

import re
import sys
import os
import math

class Player:
   def __init__(self, agaid, name, rating):
      self.agaid      = int(agaid)
      self.name       = name
      self.rating     = float(rating)
      self.round      = []
      self.new_rating = []

class Game:
   def __init__(self, white, black, winner, handicap, komi, white_rating, black_rating):
      self.white = players_byaga[white]
      self.black = players_byaga[black]
      self.winner = winner
      self.handicap = int(handicap)
      self.komi = int(komi)
      self.accel_white_rating = float(white_rating)
      self.accel_black_rating = float(black_rating)
   def my_opp(self, me):
      if self.white == me: return self.black 
      else:                return self.white
   def get_my_rating(self, me):
      if self.white == me: return self.get_white_rating()
      else:                return self.get_black_rating()
   def get_white_rating(self, use_accel_rating=1):
      if use_accel_rating: return self.accel_white_rating
      else: return self.white.rating
   def get_black_rating(self, use_accel_rating=1):
      if use_accel_rating: return self.accel_black_rating
      else: return self.black.rating
   def handi_advantage(self):
      if self.handicap == 0:
         if   self.komi ==  5: handi_advantage = 0.0
         elif self.komi ==  0: handi_advantage = 0.5
         elif self.komi == -5: handi_advantage = 1.0
         else: sys.exit("invalid self.komi:" + str(self.komi))
      else:
         handi_advantage = self.handicap - 0.5
      return handi_advantage
   def rating_advantage(self, use_accel_rating=1):
      if (self.get_white_rating() * self.get_black_rating()) < 0 : 
         return self.get_white_rating() - self.get_black_rating() - 2   # compensate for dan/kyu border
      else:
         return self.get_white_rating() - self.get_black_rating()
   def my_result(self, me):
      if self.white == me: return winner=="W"
      else:                return winner=="B"
   def white_advantage(self):
      return self.rating_advantage() - self.handi_advantage()
   def my_advantage(self, me):
      if self.white == me: return self.white_advantage()
      else:                return -self.white_advantage()

players_byaga = {}
players_byname = {}   # I'm sure there is some other awesome way, hack

f = open("register.tde")
for line in f:
   line = line.rstrip()                # strip trailing whitespace including newline
   line = re.sub("#.*", "", line)      # strip comments
   if len(line) == 0: continue         # if nothing left, continue
   m = line.split("\t")                
   agaid, name, rating = m[:3]
   player = Player(agaid, name, rating)
   players_byaga[agaid] = player
   players_byname[name] = player
f.close

f = open("TRUERATS.tde")
for line in f:
   m = re.split("\s+|=", line)
   agaid = m[0]
   truerating = float(m[2])
   players_byaga[agaid].truerating = truerating
f.close

# 1RATSWP.txt format:
#\t2.7\t\tOlsen, Andy
def parse_ratswp(filename):
   f = open(filename)
   for line in f:
      #line = line.lstrip(line.rstrip())   # why can't I do this in one step?
      line = line.lstrip()
      line = line.rstrip()
      (rating, win_loss_record, name) = re.split("\t", line)
      rating = float(rating)
      players_byname[name].new_rating.append(rating)
   f.close

round = 1
while (os.path.exists(str(round)+".tde")):
   parse_ratswp(str(round)+"RATSWP.txt")

   # X.tde format:
   # 7998 4408 B 0 5 # Olsen, Andy 2.6 : Blake, Ken -1.0
   f = open(str(round)+".tde")
   for line in f:
      line = line.rstrip()
      line = re.sub("##.*", "", line)
      if len(line) == 0: continue
      m = re.split("\s*[#:]\s*", line)
      white, black, winner, handicap, komi = re.split("\s+", m[0])
      handicap = int(handicap)
      komi = int(komi)
      white_rating = re.search("[-\d\.]+", m[1]).group()
      black_rating = re.search("[-\d\.]+", m[2]).group()
      white_rating = float(white_rating)
      black_rating = float(black_rating)
      game = Game(white, black, winner, handicap, komi, white_rating, black_rating)
      players_byaga[white].round.append(game)
      players_byaga[black].round.append(game)
   f.close
   round += 1
total_rounds = round - 1

# Parse ratings after final round
parse_ratswp("RATSWP.txt")

def tdwrap(td):
   return "<td>" + str(td) + "</td>"

print "<table border=\"1\">"
print "<tr><td>agaid</td><td>name</td><td>rating</td>",
for x in range(1, total_rounds+1): print tdwrap(x)    
print tdwrap("final")
print "</tr>"
#print tdwrap(x) for x in range(1, total_rounds+1)     # why can't I do a comprehension here?
for player in players_byaga.values():
   #for tmp in [player.agaid, player.name, player.rating, player.truerating]: print tdwrap(tmp)
   print tdwrap(player.agaid), tdwrap(player.name)
   print tdwrap("enter %0.2f" % (player.rating) + "<br>" + "true %0.2f" % (player.truerating))
   for curr_round in range(1, total_rounds+1):
      game = player.round[curr_round-1]
      print "<td>",
      assert game.get_my_rating(player) == player.new_rating[curr_round-1]
      print "my_curr_rating", game.get_my_rating(player), "<br>",
      print "opp ", game.my_opp(player).name, "<br>",
      print "opp_rating %0.2f" % (game.my_opp(player).rating), "<br>",
      print "opp_curr_rating %0.2f" % (game.get_my_rating(game.my_opp(player))), "<br>",
      print "win?", game.my_result(player), "<br>",
      print "handi", "%0.2f" % (game.handi_advantage()), "<br>",
      print "rat_diff", "%0.2f" % (game.rating_advantage()), "<br>",
      print "my_adv", "%0.2f" %(game.my_advantage(player)), "<br>",
      print "</td>"
   print tdwrap(player.new_rating[total_rounds])
   print "</tr>"
print "</table>"
