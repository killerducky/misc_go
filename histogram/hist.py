#!/usr/local/bin/python

# Usage:  hist.py
# Outputs a google chart API url 

import math
import sys

# AGA form skips all numbers (-1.0, 1)
# Linear form adds 2 to all kyu numbers to fill this gap

# k/d      AGA                 linear
# 2k = -2.99...-2.01  = +2 = -0.99..-0.01
# 1k = -1.99...-1.01  = +2 =  0.01...0.99
# 1d =  1.01....1.99  =       1.01...1.99

# AGA and KGS in AGA form
#  %       AGA      KGS      USCF    EGF
# ---   | ------ | ------ | ----- | ----- |
#  1    | -34.61 | -24.26 |   444 |   100 |
#  2    | -32.58 | -22.30 |   531 |   100 |
#  5    | -27.69 | -19.20 |   663 |   153 |
# 10    | -23.47 | -15.36 |   793 |   456 |
# 20    | -18.54 | -11.26 |   964 |   953 |
# 30    | -13.91 |  -8.94 |  1122 |  1200 |
# 40    |  -9.90 |  -7.18 |  1269 |  1387 |
# 50    |  -7.10 |  -5.65 |  1411 |  1557 |
# 60    |  -4.59 |  -4.19 |  1538 |  1709 |
# 70    |  -1.85 |  -2.73 |  1667 |  1884 |
# 80    |   2.10 |  -1.28 |  1807 |  2039 |
# 90    |   4.71 |   2.52 |  1990 |  2217 |
# 95    |   6.12 |   3.88 |  2124 |  2339 |
# 98    |   7.41 |   5.29 |  2265 |  2460 |
# 99    |   8.15 |   6.09 |  2357 |  2536 |
# 99.5  |   8.70 |   7.20 |  2470 |  2604 |
# 99.9  |   9.64 |   pro  |  2643 |  2747 |
# top   |  10.12 |    9p  |  2789 |  2809 |

# Linear for all, USCF scaled arbitrarily to fit in approximately the same range
#   %     AGA    KGS     USCF      EGF
#   1   -32.61  -22.26  -15.56   -19.00
#   2   -30.58  -20.30  -14.69   -19.00
#   5   -25.69  -17.20  -13.37   -18.47
#  10   -21.47  -13.36  -12.07   -15.44
#  20   -16.54  -9.26   -10.36   -10.47
#  30   -11.91  -6.94    -8.78    -8.00
#  40   -7.90   -5.18    -7.31    -6.13
#  50   -5.10   -3.65    -5.89    -4.43
#  60   -2.59   -2.19    -4.62    -2.91
#  70    0.15   -0.73    -3.33    -1.16
#  80    2.10    0.72    -1.93     0.39
#  90    4.71    2.52    -0.10     2.17
#  95    6.12    3.88     1.24     3.39
#  98    7.41    5.29     2.65     4.60
#  99    8.15    6.09     3.57     5.36
#  99    8.70    7.20     4.70     6.04
#  99    9.64             7.47    
# 100   10.12   10.50     7.89     8.09
# 

class Rating:
   def __init__(self, rating, style="aga"):
      if (style == "aga"):
         if rating < 0: rating -= 0.000001   # special case kyus so the borders work?  super hack!
         self.rating = self.aga2lin(rating)
      elif (style == "lin"):
         self.rating = rating
      elif (style == "dankyu"):
         self.rating = self.dankyu2lin(rating)
      else: raise
   def __str__(self, style="dankyu", precision=-1):
      if (style == "dankyu"):
         tmp = self.lin2aga(self.rating)
         if (tmp < 1): return "%d%s" % (-tmp, "k")
         else:         return "%d%s" % ( tmp, "d")
      elif (style == "aga"):
         if precision == -1: precision = 2
         return "%0.*f" % (precision, self.lin2aga(self.rating))
      elif (style == "lin"):
         if precision == -1: precision = 2
         return "%0.*f" % (precision, self.rating)
      else: 
         raise
   def lin2aga(self, rating_lin):
      if (rating_lin < 1): return rating_lin-2
      else:                return rating_lin
   def aga2lin(self, rating_aga):
      if (rating_aga < 0): return rating_aga+2
      else:                return rating_aga
   def dankyu2lin(self, rating_dankyu):
      if   (rating_dankyu[-1] == "d"): return  float(rating_dankyu[:-1]) + 0.5
      elif (rating_dankyu[-1] == "k"): return -float(rating_dankyu[:-1]) + 2 - 0.5
      else: raise
   def linear_weakest(self):
      return math.floor(self.rating)
      #if (self.rating >= 1): return math.floor(self.rating)
      #else:                  return math.floor(self.rating+1)

percent = [1,2,5,10,20,30,40,50,60,70,80,90,95,98,99,99.5]
KGS_ratings = [Rating(x, "lin") for x in [-22.26, -20.30, -17.20, -13.36, -9.26, -6.94, -5.18, -3.65, -2.19, -0.73, 0.72, 2.52, 3.88, 5.29, 6.09, 7.20]]
AGA_ratings = [Rating(x, "lin") for x in [-32.61,-30.58,-25.69,-21.47,-16.54,-11.91,-7.90,-5.10,-2.59,0.15,2.10,4.71,6.12,7.41,8.15,8.70]]
EGF_ratings = [Rating(x, "lin") for x in [-19.00,-19.00,-18.47,-15.44,-10.47,-8.00,-6.13,-4.43,-2.91,-1.16,0.39,2.17,3.39,4.60,5.36,6.04]]
USCF = [444,531,663,793,964,1122,1269,1411,1538,1667,1807,1990,2124,2265,2357,2470]

# labels are not in linear
labels_dankyu = [Rating(x, "aga") for x in [-25,-24,-23,-22,-21,-20,-19,-18,-17,-16,-15,-14,-13,-12,-11,-10,-9,-8,-7,-6,-5,-4,-3,-2,-1,1,2,3,4,5,6,7,8,9]]
labels_USCF = [500, 1000, 1500, 2000, 2500]


def scale(x, minrate=-23.99, maxrate=9.99):
   return math.floor((x-minrate)/(maxrate-minrate)*10000)/100   # should do the rounding in the display

def scale_USCF(x):
   minrate = 400.0
   maxrate = 2500.0
   return math.floor((x-minrate)/(maxrate-minrate)*10000)/100   # should do the rounding in the display

labels_USCF_scale = map(scale_USCF, labels_USCF)

USCF_scale = map(scale_USCF, USCF)

red     = "ff0000"
green   = "00ff00"
blue    = "0000ff"
magenta = "ff00ff"

url = []
url.append("http://chart.apis.google.com/chart?")
url.append("&chs=600x300")
url.append("&chtt=Rating+Histogram")
url.append("&cht=lxy")
url.append("&chdl=AGA|EGF|KGS|USCF")
url.append("&chxt=x,y,t")
url.append("&chxtc=0,-900|1,-900|2,0")
url.append("&chco=%s,%s,%s,%s" % (red, green, blue, magenta))
url.append("&chd=t:"   + ",".join([str(scale(x.rating)) for x in AGA_ratings]))
url.append("|"         + ",".join(map(str, percent)))
url.append("|"         + ",".join([str(scale(x.rating)) for x in EGF_ratings]))
url.append("|"         + ",".join(map(str, percent)))
url.append("|"         + ",".join([str(scale(x.rating)) for x in KGS_ratings]))
url.append("|"         + ",".join(map(str, percent)))
url.append("|"         + ",".join(map(str, USCF_scale)))
url.append("|"         + ",".join(map(str, percent)))
url.append("&chxl=0:|" + "|".join([x.__str__("aga", 0) for x in labels_dankyu]))
url.append("|2:|"      + "|".join(map(str, labels_USCF)))
url.append("&chxp=0,"  + ",".join([str(scale(x.linear_weakest())) for x in labels_dankyu]))
url.append("|2,"       + ",".join(map(str, labels_USCF_scale)))

print str.join("\n", url)
print



#|= [AGA] |= [EGF] |= ([GoR]) |= China |= [Japan|NihonKiin] |= [Korea|Hankuk Kiwon] |= [IGS] |= [DGS] |= [KGS|KGSGoServer] |= [ORO|cyberoro] |= [Tygem] |= [OGS] |= Player |= Date
#|      | 15k | (611)  |   |   |   | 15k |   | 11k  | 18k |   |   | karaklis        | 20090304
#|    | 11k |  |   |   |   | 12k|12k   | 6k  | 14k    |   | 9k  | [ferl]      | 20090512
#|      | 11k |        |   |   |   |     |11k|      |     |   |   | [Degan]       |20090512
#|   |  |        |   |   |   |  10k   | 8k  |  5k    |     |   |   | jedwardh   | 20090422
#| 9k   |  |  |   |   |   | |10k   | 4k  |     |   |   | cratus      | 20090304
#|      |     |        |   |   |   |     |   | 10k  | 20k |   |   | takitano        | 20081220
#|    | 7k |  |   |   |   | |  | 5k |     |   |   | yanor      | 20090421
#|      | 6k  |        |   |   |   | 7k  |   | 4k   | 6k  |   |   | [PeterHB]       | 20090303
#| 5k   |     |        |   |   |   |     |   | 7k   |     |   |   | [Impulse]       | 20090126
#| 3k   |     |        |   |   |   |     |   | 3k   |     |   |   | [JohnAspinall]  | 20081114
#| 2k   | 4k  |        |   |   |   |     |   |      |     |   |   | A. Salpietro    | 20090303
#|      | 2k  |        |   |   |   | 2k  |   | 1k   |     |   |   | [tapir]         | 20090303
#|      | 2k  | (1950)  |   |   |   |     |  | 1d   |     |   |   | Simon Zeckarias    |20090514
#|      | 3k  | (1816) |   |   |   | 2k+ | 1d | 1d  |     |   |   | Frederic Ancher | 20090319
#|      |     |        |   |   |   | 2k  |   | 1k   | 1k  |   |   | incognito_1     | 20080512
#| 1d   | 2k  |        |   |   |   |     |   | 1k   |     |   |   | [Hicham]        | 20081114
#|      | 1d  | (2097) |   |   |   |     |   |   1d |     |   |   | Sverre Haga | 20090427
#|      | 1d  | (2100)  |   |   |   | 1d  |  | 2d   |     |   |   | Tomas Lechovsky    |20090515
#|      | 1d  |        |   |   |   | 1k  |   | 1d   | 2d  |   |   | incognito_2     | 20081109
#|      |     |        |   |   |   | 1d  |   | 2d   | 3d  |   |   | explo           | 20080823
#|      | 2d  | (2140)  |   |   |   |     |  | 2d?  |     |   | 4d | [Uberdude]     | 20090517
#| (2d) |     |        |   |   |   |     |   | 1d   | 3d  |   |   | [Tartuffe]      | 20080312
#| 2d   |     |        |   |   |   |     |   | 1d   |     |   |   | [RobFerguson]   | 20081113
#| 3.0d |     |        |   |   |   | 2k+ |   | 1.2d |     |   |   | [yoyoma]        | 20090119
#| 3d   |     |        |   |   |   | 2d  |   |   2d |     |   |   | Dima Arinkin        | 20090507
#|      |     |        |   |   |   |     |   | 2d   | 5d  |   |   | gougou          | 20080312
#| 4d   |     |        |   |   |   |     |   | 3d   | 5d  |   |   | SColbert        | 20090122
#|      | 1d  |        |   |   |   |     |   | 3d   | 6d  |   |   | [nexik]         | 20081109
#|      | 2d  | (2225) |   |   |   |     |   | 4d   | 6d  |   |   | [kamyszyn]         | 20090505
#| 5d   |     |        |   |   |   |     |   | 4d   |     |   |   | sol.ch          | 20081114
#| 6d   |     |        |4d |   |   |5d-6d|4d |5d    |6d   |   |   |Nick Jhirad    |20090508
#| 6d   | 3d  | (2350) |   |   |   |     |   | 5d   |     |   |   | Wang zi Guo     | 20090303
#|    |   |  |   |   |   |     | 20k  | 14k   |     |   |   | pmurk     | 20090528
#| 5d   | 4d  | (2409) |   |   |   |     |   |      |     |   |   | Willem Mallon   | 20090303
#| 7d   | 5d  |        |   |   |   |     |   |      |     |   |   | Jean Michel     | 20090303
#| 8d   | 6d  |        |   |   |   |     |   |      |     |   |   | Robert Mateescu | 20090303
#| 8d   | 6d  |        |   |   |   |     |   |      |     |   |   | Sorin Gherman   | 20090303

#| 9k   | 4k   | cratus          | 20090304
#| 5k   | 7k   | [Impulse]       | 20090126
#| 3k   | 3k   | [JohnAspinall]  | 20081114
#| 1d   | 1k   | [Hicham]        | 20081114
#| 2d   | 1d   | [RobFerguson]   | 20081113
#| 3.0d | 1.2d | [yoyoma]        | 20090119
#| 3d   |   2d | Dima Arinkin    | 20090507
#| 4d   | 3d   | SColbert        | 20090122
#| 5d   | 4d   | sol.ch          | 20081114
#| 6d   | 5d   | Nick Jhirad     | 20090508
#| 6d   | 5d   | Wang zi Guo     | 20090303

class Point:
   def __init__(self, kgs, aga):
      self.kgs = kgs
      self.aga = aga
   def __str__(self):
      return str(self.kgs) + str(self.aga)

ratings = {}
ratings["cratus"]       = Point(Rating("9k", "dankyu"), Rating("4k", "dankyu"))
ratings["Impulse"]      = Point(Rating("5k", "dankyu"), Rating("7k", "dankyu"))
ratings["JohnAspinall"] = Point(Rating("3k", "dankyu"), Rating("3k", "dankyu"))
ratings["Hicham"]       = Point(Rating("1d", "dankyu"), Rating("1k", "dankyu"))
ratings["RobFerguson"]  = Point(Rating("2d", "dankyu"), Rating("1d", "dankyu"))
ratings["yoyoma"]       = Point(Rating("3d", "dankyu"), Rating("1d", "dankyu"))
ratings["Dima Arinkin"] = Point(Rating("3d", "dankyu"), Rating("2d", "dankyu"))
ratings["SColbert"]     = Point(Rating("4d", "dankyu"), Rating("3d", "dankyu"))
ratings["sol.ch"]       = Point(Rating("5d", "dankyu"), Rating("4d", "dankyu"))
ratings["Nick Jhirad"]  = Point(Rating("6d", "dankyu"), Rating("5d", "dankyu"))
ratings["Wang zi Guo"]  = Point(Rating("6d", "dankyu"), Rating("5d", "dankyu"))

rating_bins = {}

for name, point in ratings.items():
   key = (str(point.kgs), str(point.aga))
   rating_bins.setdefault(key, [0, point])
   rating_bins[key][0] += 1

for k, v in rating_bins.items():
   print k, v[0], v[1].kgs.rating

print

url = []
url.append("http://chart.apis.google.com/chart?")
url.append("&chs=300x300")
url.append("&chtt=Rating+Histogram")
url.append("&cht=s")
#url.append("&chdl=AGA|EGF|KGS|USCF")
#url.append("&chxt=x,y,t")
#url.append("&chxtc=0,-900|1,-900|2,0")
#url.append("&chco=%s,%s,%s,%s" % (red, green, blue, magenta))
url.append("&chd=t:"   + ",".join([str(scale(x[1].kgs.rating, -10, 9)) for x in rating_bins.values()]))
url.append("|"         + ",".join([str(scale(x[1].aga.rating, -10, 9)) for x in rating_bins.values()]))
url.append("|"         + ",".join([str(x[0]*50)                   for x in rating_bins.values()]))
#url.append("&chxp=0,"  + ",".join([str(scale(x.linear_weakest())) for x in labels_dankyu]))

print str.join("\n", url)

