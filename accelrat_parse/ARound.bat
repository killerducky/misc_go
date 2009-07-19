@echo off
rem *********************************************************
rem AccelRat 3.0.1 - Copyright (c) 1995-1999 Paul G. Matthews
rem *********************************************************

rem
rem This script updates tournament rating statistics and pairs the next round.
rem

rem Check input requirements
if X%1==X goto ARGS
if not X%2==X goto ARGS
if %1==1 goto INFILES
if %1==2 goto INFILES
if %1==3 goto INFILES
if %1==4 goto INFILES
if %1==5 goto INFILES
if %1==6 goto INFILES
if %1==7 goto INFILES
if %1==8 goto INFILES
if %1==9 goto INFILES
goto ARGS

:INFILES
if not exist REGISTER.TDE goto MISSING
goto READYGO

:MISSING
echo You should have the following files in your current directory:
echo    REGISTER.TDE       - Registered players, tournament parameters
echo    1.TDE, 2.TDE, etc. - Game records for any previous rounds
echo.

:ARGS
echo You must provide one command line argument:
echo    (1) round number (i.e., 1, 2, 3, ...)
echo For example,
echo    %0 1
echo.
goto STOPBAT

:READYGO
if not exist %1.TDE goto CLEANST
echo WARNING: %1.TDE already exists and will be erased
pause

:CLEANST
rem Erase any previous effort and temporary files
if exist %1.TDE erase %1.TDE
if exist %1RATSCW.TXT erase %1RATSCW.TXT
if exist %1RATSWP.TXT erase %1RATSWP.TXT
if exist %1RATSWEB.TXT erase %1RATSWEB.TXT
if exist %1RATSWEB.HTM erase %1RATSWEB.HTM
if exist %1PAIRSCW.TXT erase %1PAIRSCW.TXT
if exist %1PAIRSWP.TXT erase %1PAIRSWP.TXT
if exist %1PAIRSWEB.TXT erase %1PAIRSWEB.TXT
if exist %1PAIRSWEB.HTM erase %1PAIRSWEB.HTM
if exist *.LOG erase *.LOG
if exist AR$*.* erase AR$*.*

echo Processing ...

rem
rem Validate input data files.
rem

rem Check format of player register
arexe30 archeck REGISTER /tourney /out=AR$CHKR
if errorlevel 1 goto STOPBAT

rem Check format of game records for any paired rounds
if not exist 1.TDE goto GATHER
arexe30 archeck 1 /tourney /out=AR$CHK1
if errorlevel 1 goto STOPBAT
if not exist 2.TDE goto GATHER
arexe30 archeck 2 /tourney /out=AR$CHK2
if errorlevel 1 goto STOPBAT
if not exist 3.TDE goto GATHER
arexe30 archeck 3 /tourney /out=AR$CHK3
if errorlevel 1 goto STOPBAT
if not exist 4.TDE goto GATHER
arexe30 archeck 4 /tourney /out=AR$CHK4
if errorlevel 1 goto STOPBAT
if not exist 5.TDE goto GATHER
arexe30 archeck 5 /tourney /out=AR$CHK5
if errorlevel 1 goto STOPBAT
if not exist 6.TDE goto GATHER
arexe30 archeck 6 /tourney /out=AR$CHK6
if errorlevel 1 goto STOPBAT
if not exist 7.TDE goto GATHER
arexe30 archeck 7 /tourney /out=AR$CHK7
if errorlevel 1 goto STOPBAT
if not exist 8.TDE goto GATHER
arexe30 archeck 8 /tourney /out=AR$CHK8
if errorlevel 1 goto STOPBAT
if not exist 9.TDE goto GATHER
arexe30 archeck 9 /tourney /out=AR$CHK9
if errorlevel 1 goto STOPBAT

:GATHER

rem
rem Gather previous games.
rem

rem Extract game records from previously paired rounds.
arexe30 argames REGISTER /round=%1 /out=AR$GAMES
if errorlevel 1 goto STOPBAT

rem
rem Update tournament statistics.
rem

rem Calculate seed ratings based on register.
arexe30 arseeds REGISTER /out=AR$SEEDS
if errorlevel 1 goto STOPBAT

rem Calculate new ratings.
arexe30 aratings AR$GAMES AR$SEEDS /out=AR$NRATS
if errorlevel 1 goto STOPBAT

rem Count wins.
arexe30 arplyrs AR$GAMES /wins /tag=wins /tag=winfraction /out=AR$WINS
if errorlevel 1 goto STOPBAT

rem
rem Combine relevant player attributes into one file.
rem

rem Extract player name and pairing attributes from register.
arexe30 arplyrs REGISTER /tag=name /tag=bye /tag=drop /tag=avoid /tag=timezone /out=AR$ATTS
if errorlevel 1 goto STOPBAT

rem Combine player attributes
arexe30 arplyrs AR$ATTS AR$WINS AR$SEEDS AR$NRATS /out=AR$UPDT
if errorlevel 1 goto STOPBAT

rem
rem Do pairings.
rem

rem Pair players for this round.
arexe30 arpairs AR$UPDT AR$GAMES /rules=REGISTER /round=%1 /out=%1
if errorlevel 1 goto STOPBAT

rem
rem Write reports.
rem

rem Write ratings list in CW format.
arexe30 areportp AR$UPDT /tag=rating /tag=winfraction /tag=name /out=%1RATSCW
if errorlevel 1 goto STOPBAT

rem Write ratings list in WP format.
arexe30 areportp AR$UPDT /tag=rating /tag=winfraction /tag=name /wp /out=%1RATSWP
if errorlevel 1 goto STOPBAT

rem Write ratings list in HTML.
arexe30 areportp AR$UPDT /tag=rating /tag=winfraction /tag=name /html /out=%1RATSWEB
if errorlevel 1 goto STOPBAT
rename %1RATSWEB.TXT %1RATSWEB.HTM

rem Write pairings list in CW format.
arexe30 areportb %1 AR$UPDT /out=%1PAIRSCW
if errorlevel 1 goto STOPBAT

rem Write pairings list in WP format.
arexe30 areportb %1 AR$UPDT /wp /out=%1PAIRSWP
if errorlevel 1 goto STOPBAT

rem Write pairings list in HTML.
arexe30 areportb %1 AR$UPDT /html /out=%1PAIRSWEB
if errorlevel 1 goto STOPBAT
rename %1PAIRSWEB.TXT %1PAIRSWEB.HTM

rem
rem Clean up.
rem

rem Erase temporary files
erase *.LOG
erase AR$*.*

rem
rem Tell user what was output.
rem

echo Look for the following files:
echo    %1RATSCW.TXT   - Ratings list, assuming constant width font
echo    %1RATSWP.TXT   - Ratings list, with tabs for a word processor
echo    %1RATSWEB.HTM  - Ratings list, for web browser
echo    %1PAIRSCW.TXT  - Pairings list, assuming constant width font
echo    %1PAIRSWP.TXT  - Pairings list, with tabs for a word processor
echo    %1PAIRSWEB.HTM - Pairings list, for web browser
echo    %1.TDE         - Paired game records, in TDE format

goto DONE

:STOPBAT
echo Script execution stopped due to error.

:DONE

