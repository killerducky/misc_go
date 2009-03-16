#!/usr/bin/perl


use Getopt::Std;
use LWP::Simple;
use Data::Dumper;
$Data::Dumper::Indent = 1;
#print Dumper($tdb);

getopts( "hst:k:", \%opt ) or usage();
usage() if $opt{h};


$KGS     = "http://www.gokgs.com";
$SLEEP   = 1;
$SLEEP   = $opt{s} if (defined $opt{s});
$KEEP    = $opt{k};
$UNFINISHED_RESULT = -1;

sub usage {
   die <<EOP;
kgs_tourny.pl -t <tournyid> [-s secs] [-k keep]
   -t   <tournyid>
   -s   number sleep seconds default=1
   -k   keep rounds 1 through k.  -1 means keep all.
EOP
}

$KGS_TID = $opt{t} or usage();

if ($KEEP != -1) {
   $pagename = "$KGS/tournInfo.jsp?id=$KGS_TID";
   $tournInfoPage = get "$pagename" or die "could not open $pagename";
   sleep $SLEEP;
   open OUT, ">tournInfo_$KGS_TID.html";
   print OUT $tournInfoPage;
   close OUT;
   @links = $tournInfoPage =~ m/a href="(.*?)"/g;
   foreach $link (@links) {
      next if ($link !~ /tournGames/);
      #print "link|$_|\n";
      $link =~ s/&amp;/&/g;
      ($round) = $link =~ /round=(\d+)/;
      if ($round > $KEEP) {
         $tournGamesPages[$round] = get "$KGS/$link" or die;
         sleep $SLEEP;
         open OUT, ">tournGames_${KGS_TID}_$round.html";
         print OUT $tournGamesPages[$round];
         close OUT;
      }
   }
}

$tournInfoPage = do { local( @ARGV, $/ ) = "tournInfo_$KGS_TID.html" ; <> } ;<IN>;
@links = $tournInfoPage =~ m/a href="(.*?)"/g;
foreach $link (@links) {
   next if ($link !~ /tournGames/);
   #"link|$_|\n";
   $link =~ s/&amp;/&/g;
   ($round) = $link =~ /round=(\d+)/;
   $tournGamesPages[$round] = do { local( @ARGV, $/ ) = "tournGames_${KGS_TID}_$round.html" ; <> } ;<IN>;
}

#|<td><a href="http://files.gokgs.com/games/2008/3/10/aquadude-oldbob.sgf">Download</a></td>|
#|<td class="name">aquadude [1k]</td>|
#|<td class="name">oldbob [1k]</td>|
#|<td>19Ã19 </td>|
#|<td>3/10/08 3:05 AM</td>|
#|<td>B+Res.</td>|

#        0                                           1                     2
#|<td>&nbsp;</td>|<td colspan="2" class="name">Parabol [2k]</td>|<td colspan="3">Bye (No show)</td>

#|<td>&nbsp;</td>|<td class="name">Arctic [4d]</td>|<td class="name">Nickless [2k]</td>|<td>19Ã19 </td>|<td>1/1/70 12:00 AM</td>|<td>Unfinished</td>

foreach $link (@links) {
   next if ($link !~ /tournGames/);
   #print "link|$_|\n";
   $link =~ s/&amp;/&/g;
   ($round) = $link =~ /round=(\d+)/;
   $tdb{rounds}{$round}{unfinished} = 0;
   foreach $row (split /(<tr>.*?<\/tr>)/, $tournGamesPages[$round]) {
      # skip uninteresting lines
      next if ($row !~ /<tr>.*?<\/tr>/);
      next if ($row =~ m#Next round#);
      next if ($row =~ m#Previous round#);
      next if ($row =~ m#Start Time#);
      $td_regexp = "<td.*?>.*?<\/td>";
      @td = grep (/$td_regexp/, (split /($td_regexp)/, $row));
      if (0) {
      } elsif ( ($td[2] =~ m#<td colspan="3">Bye \(No show\)</td>#) ||
                ($td[2] =~ m#<td colspan="3">Bye \(Requested\)</td>#)) {
         foreach (@td) { s/<td.*?>//; s/<\/td>//; }
         $name = $td[1];
         $tdb{names}{$name}{rounds}{$round}{result} = 0.5;
         $tdb{names}{$name}{rounds}{$round}{opp} = "bye";  # be careful no one is named "bye".  For now works because real names always have [rank] in them.
      } elsif ($td[2] =~ m#<td colspan="3">Bye</td>#  ) {
         foreach (@td) { s/<td.*?>//; s/<\/td>//; }
         $name = $td[1];
         $tdb{names}{$name}{rounds}{$round}{result} = 1;
         $tdb{names}{$name}{rounds}{$round}{opp} = "bye";
      } else {
         foreach (@td) { s/<td.*?>//; s/<\/td>//; }
         ($sgf, $w_name, $b_name, $size, $date, $result) = @td;
         if ($sgf ne "&nbsp;") {
            ($sgf) = $sgf =~ m#"(http:.*?)"#;
         }
         $tdb{names}{$w_name}{rounds}{$round}{opp} = $b_name;
         $tdb{names}{$b_name}{rounds}{$round}{opp} = $w_name;
         $tdb{names}{$w_name}{rounds}{$round}{sgf} = $sgf;
         $tdb{names}{$b_name}{rounds}{$round}{sgf} = $sgf;
         if ($result =~ /Unfinished/) {
            $tdb{names}{$w_name}{rounds}{$round}{result} = $UNFINISHED_RESULT;
            $tdb{names}{$b_name}{rounds}{$round}{result} = $UNFINISHED_RESULT;
            $tdb{rounds}{$round}{unfinished} = 1;
         } else {
            ($winner, $winby) = $result =~ m#([BW])\+(.*?)#;
            $tdb{names}{$w_name}{rounds}{$round}{result} = $winner eq "W" ? 1 : 0;
            $tdb{names}{$b_name}{rounds}{$round}{result} = $winner eq "B" ? 1 : 0;
         }
      }
      #print "$round $row\n" if ($name =~ /test/);
   }
}

$last_unfinished = 0;
$last_round      = 0;
foreach $round (sort numeric keys %{$tdb{rounds}}) {
   if (!$tdb{rounds}{$round}{unfinished}) {
      $last_unfinished = $round;
   }
   $last_round = $round;
}

foreach $name (keys %{$tdb{names}}) {
   my $sum = 0;
   #my $sos = 0;
   foreach $round (1..$last_round) {
      if (!defined $tdb{names}{$name}{rounds}{$round}{result}) {
         $tdb{names}{$name}{rounds}{$round}{total} = $sum;
      } elsif ($tdb{names}{$name}{rounds}{$round}{result} == $UNFINISHED_RESULT) {
         #$sum - no change
         #$sos += $sos;
         $tdb{names}{$name}{rounds}{$round}{total} = $sum;
         #$tdb{names}{$name}{rounds}{$round}{sos} = $sos;
      } else {
         $sum += $tdb{names}{$name}{rounds}{$round}{result};
         #$sos += $sum;
         $tdb{names}{$name}{rounds}{$round}{total} = $sum;
         #$tdb{names}{$name}{rounds}{$round}{sos} = $sos;
      }
   }
   $tdb{names}{$name}{total} = $sum;
}



open OUT, ">tournXtable_$KGS_TID.html";
print OUT "This is a crosstable of results for a KGS tournament #$KGS_TID.<br><br>\n";
print OUT "In this format you can see who played who and the result for each round in one page.<br><br>\n";
print OUT "<a href=http://www.gokgs.com/tournEntrants.jsp?sort=s&id=$KGS_TID>Official KGS tournament results</a><br>\n";
print OUT "Definition of <a href=http://senseis.xmp.net/?SOS>SOS tiebreaker</a><br>\n";
print OUT "Definition of <a href=http://senseis.xmp.net/?SODOS>SODOS tiebreaker</a><br>\n";
print OUT "<br>\n";
print OUT "bye= means the player requested a half-point bye<br>\n";
print OUT "bye+ means the player got a full-point bye (due to odd number of players)<br>\n";
if ($last_unfinished != $last_round) {
   print OUT "Round #$last_round is in progress.<br>\n";
   print OUT "Sorted by number of points in the last complete round, #$last_unfinished.<br>\n";
   print OUT "SOS and SODOS tiebreaks are as of round $last_unfinished.<br>\n";
}
print OUT "<br>\n";

printf OUT "<table border=\"1\"><tr><td>%3s</td> <td>%20s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>", "id", "name", "played", "won", "lost", "full<br>bye";
foreach $round (sort numeric keys %{$tdb{rounds}}) {
   printf OUT "  <td>%6s</td>", "rnd $round" . ($tdb{rounds}{$round}{unfinished} ? "*" : "");
}
print OUT "<td><a href=http://senseis.xmp.net/?SOS>sos</a></td>\n";
print OUT "<td><a href=http://senseis.xmp.net/?SODOS>sodos</a></td></tr>\n";

foreach $name (keys %{$tdb{names}}) {
   my $sodos = 0;
   my $sos   = 0;
   my $rounds_played = 0;
   my $num_win     = 0;
   my $num_loss    = 0;
   my $num_fullbye = 0;
   foreach $round (1..$last_unfinished) {
      my $opp = $tdb{names}{$name}{rounds}{$round}{opp};
      if (defined $opp && $opp ne "bye") {
         $sos += $tdb{names}{$opp}{rounds}{$last_unfinished}{total};
         if ($tdb{names}{$name}{rounds}{$round}{result} == 1) {
            $sodos += $tdb{names}{$opp}{rounds}{$last_unfinished}{total};
            $num_win++;
         } elsif ($tdb{names}{$name}{rounds}{$round}{result} == 0) {
            $num_loss++;
         }
         $rounds_played++;
      } elsif ($tdb{names}{$name}{rounds}{$round}{result} == 1) {
         # 1 point bye counts as played
         $rounds_played++;
         $num_fullbye++;
      }
   }
   $tdb{names}{$name}{sos}   = $sos;
   $tdb{names}{$name}{sodos} = $sodos;
   $tdb{names}{$name}{rounds_played} = $rounds_played;
   $tdb{names}{$name}{num_win}       = $num_win;
   $tdb{names}{$name}{num_loss}      = $num_loss;
   $tdb{names}{$name}{num_fullbye}   = $num_fullbye;
}

$place = 1;
foreach $name (sort bytotal keys %{$tdb{names}}) {
   $tdb{names}{$name}{place} = $place;
   $place++;
}



foreach $name (sort bytotal keys %{$tdb{names}}) {
   printf OUT "<tr><td>%s</td> <td>%s</td> <td>%s</td> <td>%s</td> <td>%s</td> <td>%s</td>", 
      $tdb{names}{$name}{place}, 
      $name, 
      $tdb{names}{$name}{rounds_played},
      $tdb{names}{$name}{num_win},
      $tdb{names}{$name}{num_loss},
      $tdb{names}{$name}{num_fullbye};
   foreach $round (sort numeric keys %{$tdb{names}{$name}{rounds}}) {
      $opp = $tdb{names}{$name}{rounds}{$round}{opp};
      if (!defined $opp) {
         $oppid = "x";
         $sgflink  = "";
      }
      elsif ($opp eq "bye") {
         $oppid = "bye";
         $sgflink  = "";
      } 
      elsif ($tdb{names}{$name}{rounds}{$round}{sgf} eq "&nbsp;") {
         $oppid = $tdb{names}{$opp}{place};
         $sgflink = "";
      } else {
         $oppid = $tdb{names}{$opp}{place};
         $sgflink = "<a href=$tdb{names}{$name}{rounds}{$round}{sgf}>";
      }
      printf OUT "  <td>%s%3s%s %5s%s</td>", 
         $sgflink,
         $oppid, 
         &resultstring($tdb{names}{$name}{rounds}{$round}{result}), 
         &totalstring($tdb{names}{$name}{rounds}{$round}{total}),
         $sgflink ? "" : "</a>";
   }
   printf OUT "<td>%0.1f</td>", $tdb{names}{$name}{sos};
   printf OUT "<td>%0.1f</td>", $tdb{names}{$name}{sodos};
   print OUT "</tr>\n";
}

print OUT "</table>\n";
exit;


sub resultstring {
   my $resultint = shift @_;
   return ($resultint ==   1) ? "+" : 
          ($resultint ==   0) ? "-" : 
          ($resultint == 0.5) ? "=" : 
          ($resultint == $UNFINISHED_RESULT) ? "*" : "ERR";
}

sub totalstring {
   my $totalint = shift @_;
   if ($totalint == $UNFINISHED_RESULT) {
      return "*";
   } else {
      return sprintf "%3.1f", $totalint;
   }
}

sub bytotal {
   if ($last_unfinished == 0) {
      $b <=> $a;  # probably sort by rank first, also there is mcmahon to think about
   } else {
      $tdb{names}{$b}{rounds}{$last_unfinished}{total} <=> $tdb{names}{$a}{rounds}{$last_unfinished}{total} or
      $tdb{names}{$b}{sos}   <=> $tdb{names}{$a}{sos} or
      $tdb{names}{$b}{sodos} <=> $tdb{names}{$a}{sodos} or
      uc($a) cmp uc($b);

      #$result = ($tdb{names}{$b}{rounds}{$last_unfinished}{total} <=> $tdb{names}{$a}{rounds}{$last_unfinished}{total});
      #return $result if ($result !=0);
      #$result = ($tdb{names}{$b}{sos}   <=> $tdb{names}{$a}{sos});
      #return $result if ($result !=0);
      #$result =  ($tdb{names}{$b}{sodos} <=> $tdb{names}{$a}{sodos});
      #return $result if ($result !=0);
      #if ($result == 0) {
      #   $result = uc($a) cmp uc($b);
      #}
      #return $result;
   }
}


sub numeric {
   $a <=> $b;
}
