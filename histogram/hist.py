#!/usr/local/bin/python

# Usage:  hist.py
# Outputs a google chart API url 

import math

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


percent = [1,2,5,10,20,30,40,50,60,70,80,90,95,98,99,99.5]
KGS_linear = [-22.26, -20.30, -17.20, -13.36, -9.26, -6.94, -5.18, -3.65, -2.19, -0.73, 0.72, 2.52, 3.88, 5.29, 6.09, 7.20]
AGA_linear = [-32.61,-30.58,-25.69,-21.47,-16.54,-11.91,-7.90,-5.10,-2.59,0.15,2.10,4.71,6.12,7.41,8.15,8.70]
EGF_linear = [-19.00,-19.00,-18.47,-15.44,-10.47,-8.00,-6.13,-4.43,-2.91,-1.16,0.39,2.17,3.39,4.60,5.36,6.04]
USCF = [444,531,663,793,964,1122,1269,1411,1538,1667,1807,1990,2124,2265,2357,2470]


# labels are not in linear
labels_AGA = [-25,-24,-23,-22,-21,-20,-19,-18,-17,-16,-15,-14,-13,-12,-11,-10,-9,-8,-7,-6,-5,-4,-3,-2,-1,1,2,3,4,5,6,7,8,9]
labels_USCF = [500, 1000, 1500, 2000, 2500]

minrate = -23.99  # weakest 25k
maxrate = 9.99    # strongest 9d

#def scale(x, min, max):
def scale(x):
   return math.floor((x-minrate)/(maxrate-minrate)*10000)/100   # should do the rounding in the display

def scale_USCF(x):
   minrate = 400.0
   maxrate = 2500.0
   return math.floor((x-minrate)/(maxrate-minrate)*10000)/100   # should do the rounding in the display

def linear_weakest(x):
   if (x<0):
      return x+1
   if (x>0):
      return x

labels_weakest = map(linear_weakest, labels_AGA)
labels_scale = map(scale, labels_weakest)

labels_USCF_scale = map(scale_USCF, labels_USCF)

KGS_scale = map(scale, KGS_linear)
AGA_scale = map(scale, AGA_linear)
EGF_scale = map(scale, EGF_linear)
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
url.append("&chd=t:" + str.join(",", map(str, AGA_scale)))
url.append("|"       + str.join(",", map(str, percent)))
url.append("|"       + str.join(",", map(str, EGF_scale)))
url.append("|"       + str.join(",", map(str, percent)))
url.append("|"       + str.join(",", map(str, KGS_scale)))
url.append("|"       + str.join(",", map(str, percent)))
url.append("|"       + str.join(",", map(str, USCF_scale)))
url.append("|"       + str.join(",", map(str, percent)))
url.append("&chxl=0:|" + str.join("|", map(str, labels_AGA)))
url.append("|2:|" + str.join("|", map(str, labels_USCF)))
url.append("&chxp=0," + str.join(",", map(str, labels_scale)))
url.append("|2," + str.join(",", map(str, labels_USCF_scale)))

print str.join("\n", url)


