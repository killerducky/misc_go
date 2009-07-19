#!/usr/bin/env python2.6

import re
import sys
import os
import math
import operator

# globals
players_byaga = {}
players_byname = {}   # I'm sure there is some other awesome way, hack

VERBOSE = 1

class Player:
   def __init__(self, agaid, name, rating):
      self.agaid      = int(agaid)
      self.name       = name
      self.rating     = float(rating)
      self.round      = {}
      self.new_rating = {}

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
   def get_my_rating(self, me, use_accel_rat=1):
      if self.white == me: return self.get_white_rating(use_accel_rat)
      else:                return self.get_black_rating(use_accel_rat)
   def get_white_rating(self, use_accel_rat=1):
      if use_accel_rat: return self.accel_white_rating
      else: return self.white.rating
   def get_black_rating(self, use_accel_rat=1):
      if use_accel_rat: return self.accel_black_rating
      else: return self.black.rating
   def handi_advantage(self):
      if self.handicap == 0:
         if   self.komi >  0: handi_advantage = 0.0
         elif self.komi == 0: handi_advantage = 0.5
         elif self.komi <  0: handi_advantage = 1.0
         else: sys.exit("invalid self.komi:" + str(self.komi))
      else:
         handi_advantage = self.handicap - 0.5
      return handi_advantage
   def rating_advantage(self, use_accel_rat=1):
      if (self.get_white_rating(use_accel_rat) * self.get_black_rating(use_accel_rat)) < 0 : 
         return self.get_white_rating(use_accel_rat) - self.get_black_rating(use_accel_rat) - 2   # compensate for dan/kyu border
      else:
         return self.get_white_rating(use_accel_rat) - self.get_black_rating(use_accel_rat)
   def my_result(self, me):
      if self.white == me: return self.winner=="W"
      else:                return self.winner=="B"
   def white_advantage(self, use_accel_rat=1):
      return self.rating_advantage(use_accel_rat) - self.handi_advantage()
   def my_advantage(self, me, use_accel_rat=1):
      if self.white == me: return self.white_advantage(use_accel_rat)
      else:                return -self.white_advantage(use_accel_rat)

# 1RATSWP.txt format:
#\t2.7\t\tOlsen, Andy
def parse_ratswp(round, filename):
   f = open(filename)
   for line in f:
      #line = line.lstrip(line.rstrip())   # why can't I do this in one step?
      line = line.lstrip()
      line = line.rstrip()
      (rating, win_loss_record, name) = re.split("\t", line)
      rating = float(rating)
      players_byname[name].new_rating[round] = rating
   f.close

def tdwrap(td):
   return "<td>" + str(td) + "</td>"

def main():
   f = open("register.tde")
   for line in f:
      line = line.rstrip()                # strip trailing whitespace including newline
      line = re.sub("#.*", "", line)      # strip comments
      if len(line) == 0: continue         # if nothing left, continue
      if re.search('"', line):
         agaid  = re.search('^(\d+)', line).group(1)
         name   = re.search('name="(.*?)"', line, re.I).group(1)
         rating = re.search('rating="(.*?)"', line, re.I).group(1)
      else:
         agaid, name, rating = line.split("\t")[:3]
         #agaid, name, rating = m[:3]
      player = Player(agaid, name, rating)
      players_byaga[agaid] = player
      players_byname[name] = player
   f.close

   #f = open("TRUERATS.tde")
   #for line in f:
   #   m = re.split("\s+|=", line)
   #   agaid = m[0]
   #   truerating = float(m[2])
   #   players_byaga[agaid].truerating = truerating
   #f.close

   round = 1
   while (os.path.exists(str(round)+".tde")):
      filename = str(round)+"RATSWP.txt"
      parse_ratswp(round, filename)

      # X.tde format:
      # 7998 4408 B 0 5 # Olsen, Andy 2.6 : Blake, Ken -1.0
      f = open(str(round)+".tde")
      for line in f:
         line = line.rstrip()
         m = re.search("## BYE (\d+)", line)
         if m:
            players_byaga[m.group(1)].round[round] = None
         else:
            line = re.sub("##.*", "", line)
            if len(line) == 0: continue
            m = re.split("\s*[#:]\s*", line)
            white, black, winner, handicap, komi = re.split("\s+", m[0])
            handicap = int(handicap)
            komi = int(komi)
            white_rating = re.search("[-\d]+\.[\d]+", m[1]).group()
            black_rating = re.search("[-\d]+\.[\d]+", m[2]).group()
            white_rating = float(white_rating)
            black_rating = float(black_rating)
            game = Game(white, black, winner, handicap, komi, white_rating, black_rating)
            players_byaga[white].round[round] = game
            players_byaga[black].round[round] = game
      f.close
      round += 1
   total_rounds = round - 1

   # Parse ratings after final round
   parse_ratswp(total_rounds+1, "RATSWP.txt")

   print "<table border=\"1\">"
   print "<tr><td>agaid</td><td>name</td><td>rating</td>",
   for x in range(1, total_rounds+1): print tdwrap(x)    
   print tdwrap("final")
   print "</tr>"
   players = players_byaga.values();
   players.sort(key=operator.attrgetter("rating"), reverse=True)
   for player in players:
      print tdwrap(player.agaid), tdwrap(player.name)
      print "<td>",
      print "enter %0.2f" % (player.rating) + "<br>"
      if total_rounds+1 in player.new_rating:
         print "final", player.new_rating[total_rounds+1]
      print "</td>"
      for curr_round in range(1, total_rounds+1):
         print "<td>",
         if curr_round in player.round and player.round[curr_round] != None:
            game = player.round[curr_round]
            # I think this only broke because a player entered and never played
            #assert game.get_my_rating(player) == player.new_rating[curr_round]
            if VERBOSE:
               print "my_curr_rating", game.get_my_rating(player), "<br>",
               print "opp ", game.my_opp(player).name, "<br>",
               print "opp_rating %0.2f" % (game.my_opp(player).rating), "<br>",
               print "opp_curr_rating %0.2f" % (game.get_my_rating(game.my_opp(player))), "<br>",
               print "win?", game.my_result(player), "<br>",
               print "handi", "%0.2f" % (game.handi_advantage()), "<br>",
               print "curr_rat_diff", "%0.2f" % (game.rating_advantage()), "<br>",
               print "curr_my_adv", "%0.2f" %(game.my_advantage(player)), "<br>",
               print "init_rat_diff", "%0.2f" % (game.rating_advantage(0)), "<br>",
               print "init_my_adv", "%0.2f" %(game.my_advantage(player, 0)), "<br>",
            else:
               print "opp ", game.my_opp(player).name, "<br>",
               if game.handi_advantage() < 1.5:
                  print "handi=", "%0.1f" % (game.handi_advantage()), "<br>",
               else:
                  print "handi=", "%0.0f" % (game.handi_advantage()+0.5), "<br>",
               print ("lose", "win")[game.my_result(player)], "<br>",
         else:
            print "BYE <br>",
            if curr_round in player.new_rating:
               print "my_curr_rating", player.new_rating[curr_round], "<br>",
            else:
               print "my_curr_rating", "XXX", "<br>",
         print "</td>"
      if total_rounds+1 in player.new_rating:
         print tdwrap(player.new_rating[total_rounds+1])
      else:
         print tdwrap("XXX")
      print "</tr>"
   print "</table>"

main()
