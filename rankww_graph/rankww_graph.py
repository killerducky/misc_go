#!/usr/bin/python

import re
import numpy as np
import matplotlib
import matplotlib.pyplot as plt


# AGA     EGF     (GoR)        IGS     DGS     KGS     ORO Player          Date
# 9k                                   10k     4k          cratus          20090304
#         15k     (611)        15k             11k         karaklis        20090304
#                                              10k     20k takitano        20081220
# 5k                                           7k          Impulse         20090126
#                              10k     8k      5k          jedwardh        20090422
#         7k                                   5k          yanor           20090421
#         6k                   7k              4k      6k  PeterHB         20090303
# 3k                                           3k          JohnAspinall    20081114
# 2k      4k                                               A. Salpietro    20090303
#         2k                   2k              1k          tapir           20090303
# 1d      2k                                   1k          Hicham          20081114
#                              2k              1k      1k  incognito_1     20080512
#         3k      (1816)       2k+     1d      1d          Frederic Ancher 20090319
# (2d)                                         1d      3d  Tartuffe        20080312
# 2d                                           1d          RobFerguson     20081113
# 3.0d                         2k+             1.2d        yoyoma          20090119
# 3d                           2d              2d          Dima Arinkin    20090507
#         1d      (2097)                       1d          Sverre Haga     20090427
#         1d                   1k              1d      2d  incognito_2     20081109
#                              1d              2d      3d  explo           20080823
#                                              2d      5d  gougou          20080312
# 4d                                           3d      5d  SColbert        20090122
#         1d                                   3d      6d  nexik           20081109
#         2d      (2225)                       4d      6d  kamyszyn        20090505
# 5d                                           4d          sol.ch          20081114
# 6d      3d      (2350)                       5d          Wang zi Guo     20090303
# 5d      4d      (2409)                                   Willem Mallon   20090303
# 7d      5d                                               Jean Michel     20090303
# 8d      6d                                               Robert Mateescu 20090303
# 8d      6d                                               Sorin Gherman   20090303
# 6d                           5d-6d   4d      5d      6d  Nick Jhirad     20090508 

def rank2rating(rank):
   m = re.match('(\d+)([dk])$', rank, re.I)
   if m:
      if m.group(2) == "d":
         return int(m.group(1)) + 0.5
      else:
         print m.group(1), m.group(2)
         return -int(m.group(1)) + 0.5
   else:
      return "error"


kgs_ranks = [ "11k",  "5k", "4k", "1k", "1k",  "1d",  "1d", "2d", "1d", "2d" ]
#igs_ranks = [ "15k", "10k", "7k", "2k", "2k", "2k+", "2k+", "2d", "1k", "1d" ]
igs_ranks = [ "15k", "10k", "7k", "2k", "2k", "2k", "2k", "2d", "1k", "1d" ]

kgs_ratings = map(rank2rating, kgs_ranks)
igs_ratings = map(rank2rating, igs_ranks)

print kgs_ratings
print igs_ratings

fig = plt.figure()
ax = fig.add_subplot(111)
#ax.plot(10*np.random.randn(100), 10*np.random.randn(100), 'o')
ax.plot(kgs_ratings, igs_ratings, '+')
ax.plot([-15,6], [-15, 6])
ax.set_title("test")
plt.show()

