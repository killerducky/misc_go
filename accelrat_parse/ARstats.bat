@echo off
rem *********************************************************
rem AccelRat 3.0.1 - Copyright (c) 1995-1999 Paul G. Matthews
rem *********************************************************

rem
rem This script calculates statistics for award purposes
rem at the conclusion of a tournament.
rem

rem Check input requirements
if not X%1==X goto ARGS
if not exist REGISTER.TDE goto MISSING
goto READYGO

:MISSING
echo You should have the following files in your current directory:
echo    REGISTER.TDE       - Registered players
echo    1.TDE, 2.TDE, etc. - Game results for each round
echo.

:ARGS
echo No command line arguments are expected.
echo.
goto STOPBAT

:READYGO

rem Erase any previous efforts and temporary files
if exist SEND2AGA.TDE erase SEND2AGA.TDE
if exist GAMESTAT.TXT erase GAMESTAT.TXT
if exist GAMESTAT.HTM erase GAMESTAT.HTM
if exist RATSCW.TXT erase RATSCW.TXT
if exist RATSWP.TXT erase RATSWP.TXT
if exist RATSWEB.TXT erase RATSWEB.TXT
if exist RATSWEB.HTM erase RATSWEB.HTM
if exist WINNERS.TXT erase WINNERS.TXT
if exist TOPGROUP.TXT erase TOPGROUP.TXT
if exist *.LOG erase *.LOG
if exist AR$*.* erase AR$*.*

echo Processing ...

rem
rem Validate format of input data files.
rem

rem Check format of player register.
arexe30 archeck REGISTER /out=AR$CHKR
if errorlevel 1 goto STOPBAT

rem Check format of game records.
if not exist 1.TDE goto GATHER
arexe30 archeck 1 /out=AR$CHK1
if errorlevel 1 goto STOPBAT
if not exist 2.TDE goto GATHER
arexe30 archeck 2 /out=AR$CHK2
if errorlevel 1 goto STOPBAT
if not exist 3.TDE goto GATHER
arexe30 archeck 3 /out=AR$CHK3
if errorlevel 1 goto STOPBAT
if not exist 4.TDE goto GATHER
arexe30 archeck 4 /out=AR$CHK4
if errorlevel 1 goto STOPBAT
if not exist 5.TDE goto GATHER
arexe30 archeck 5 /out=AR$CHK5
if errorlevel 1 goto STOPBAT
if not exist 6.TDE goto GATHER
arexe30 archeck 6 /out=AR$CHK6
if errorlevel 1 goto STOPBAT
if not exist 7.TDE goto GATHER
arexe30 archeck 7 /out=AR$CHK7
if errorlevel 1 goto STOPBAT
if not exist 8.TDE goto GATHER
arexe30 archeck 8 /out=AR$CHK8
if errorlevel 1 goto STOPBAT
if not exist 9.TDE goto GATHER
arexe30 archeck 9 /out=AR$CHK9
if errorlevel 1 goto STOPBAT

:GATHER

rem
rem Gather data needed for rating.
rem

rem Get rateable games from all rounds.
arexe30 argames /allrounds /winner /out=AR$GAMES
if errorlevel 1 goto STOPBAT

rem Calculate seed ratings and sigmas based on registration.
arexe30 arseeds REGISTER /out=AR$SEEDS
if errorlevel 1 goto STOPBAT

rem Extract player name attributes.
arexe30 arplyrs REGISTER /tag=name /out=AR$NAMES
if errorlevel 1 goto STOPBAT

rem Combine names and seed ratings for players who have games.
arexe30 arplyrs AR$NAMES AR$SEEDS /ids=AR$GAMES /out=AR$PLYRS
if errorlevel 1 goto STOPBAT

rem Get tournament label from register.
arexe30 argames REGISTER /out=AR$LABEL
if errorlevel 1 goto STOPBAT

rem Combine tournament label, player attributes, and games into one file.
rem wineconsole doesn't like the "+" operator for copy.  Use alternate method.
rem copy AR$LABEL.TDE+AR$GAMES.TDE+AR$PLYRS.TDE SEND2AGA.TDE /b
copy AR$LABEL.TDE SEND2AGA.TDE /b
type AR$GAMES.TDE >> SEND2AGA.TDE
type AR$PLYRS.TDE >> SEND2AGA.TDE
if errorlevel 1 goto STOPBAT

rem
rem Update tournament statistics.
rem

rem Calculate new rating statistics.
arexe30 aratings SEND2AGA /out=AR$NRATS
if errorlevel 1 goto STOPBAT

rem Count wins.
arexe30 arplyrs SEND2AGA /wins /tag=wins /tag=winfraction /out=AR$WINS
if errorlevel 1 goto STOPBAT

rem Combine updated player attributes into one file.
arexe30 arplyrs SEND2AGA AR$WINS AR$NRATS /out=AR$UPDT
if errorlevel 1 goto STOPBAT

rem
rem Write reports.
rem

rem Write individual game statistics.
arexe30 areportg SEND2AGA AR$NRATS /precision=1 /html /out=GAMESTAT
if errorlevel 1 goto STOPBAT
rename GAMESTAT.TXT GAMESTAT.HTM

rem Write ratings list in CW format.
arexe30 areportp AR$UPDT /tag=rating /tag=winfraction /tag=name /out=RATSCW
if errorlevel 1 goto STOPBAT

rem Write ratings list in WP format.
arexe30 areportp AR$UPDT /tag=rating /tag=winfraction /tag=name /wp /out=RATSWP
if errorlevel 1 goto STOPBAT

rem Write ratings list in HTML.
arexe30 areportp AR$UPDT /tag=rating /tag=winfraction /tag=name /html /out=RATSWEB
if errorlevel 1 goto STOPBAT
rename RATSWEB.TXT RATSWEB.HTM

rem Write general awards list.
arexe30 areportp AR$UPDT /tag=wins /tag=field /tag=name /precision=5 /out=WINNERS
if errorlevel 1 goto STOPBAT

rem Write championship top group list.
arexe30 areportp AR$UPDT /tag=field /tag=winfraction /tag=id /tag=name /precision=5 /out=TOPGROUP
if errorlevel 1 goto STOPBAT

rem
rem Clean up.
rem

rem Erase temporary files
erase *.LOG
erase AR$*.*

rem
rem Tell the user what was output.
rem

echo Look for the following output files:
echo    SEND2AGA.TDE - All tournament data needed for rating
echo    GAMESTAT.HTM - Report showing each player's tournament games
echo    RATSCW.TXT   - Updated ratings list, assuming constant width font
echo    RATSWP.TXT   - Updated ratings list, with tabs for word processor
echo    RATSWEB.HTM  - Updated ratings list, for web browser
echo    WINNERS.TXT  - Players ordered by number of wins
echo    TOPGROUP.TXT - Players ordered by field strength

goto DONE

:STOPBAT
echo Script execution stopped due to error.

:DONE

