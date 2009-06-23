@echo off
rem *********************************************************
rem AccelRat 3.0.1 - Copyright (c) 1995-1999 Paul G. Matthews
rem *********************************************************

rem
rem This script calculates local club ratings.
rem

rem Check input requirements
if X%1==X goto ARGS
if X%2==X goto ARGS
if X%3==X goto ARGS
if not X%4==X goto ARGS
goto READYGO

:ARGS
echo The following 3 command line arguments are expected:
echo    1. old base ratings file
echo    2. new tournament data file
echo    3. new base ratings file
echo For example,
echo    %0 oldbase tourney newbase
echo.
goto STOPBAT

:READYGO
rem Verify existence of old base ratings file.
if exist %1.TDE goto RG1
echo %1.TDE not found
goto STOPBAT
 
:RG1
rem Verify existence of tournament data file.
if exist %2.TDE goto RG2
echo %2.TDE not found
goto STOPBAT
 
:RG2
rem Pause if new base ratings file already exists.
if not exist %3.TDE goto RG3
echo WARNING: %3.TDE already exists and will be erased
pause
erase %3.TDE

:RG3
rem Erase any previous efforts and temporary files
if exist RATSCW.TXT erase RATSCW.TXT
if exist RATSWP.TXT erase RATSWP.TXT
if exist RATSWEB.TXT erase RATSWEB.TXT
if exist RATSWEB.HTM erase RATSWEB.HTM
if exist GAMESTAT.TXT erase GAMESTAT.TXT
if exist GAMESTAT.HTM erase GAMESTAT.HTM
if exist *.LOG erase *.LOG
if exist AR$*.* erase AR$*.*

echo Processing ...

rem
rem Validate format of input data files.
rem

rem Check format of base ratings data.
arexe30 archeck %1 /out=AR$CHK1
if errorlevel 1 goto STOPBAT

rem Check format of tournament data.
arexe30 archeck %2 /out=AR$CHK2
if errorlevel 1 goto STOPBAT

rem
rem Gather tournament data needed for rating update.
rem

rem Get rateable games.
arexe30 argames %2 /winner /stones=0,9 /komi=-9,9 /out=AR$GAMES
if errorlevel 1 goto STOPBAT

rem Get IDs of tournament players with rateable games.
arexe30 arplyrs AR$GAMES /out=AR$PIDS
if errorlevel 1 goto STOPBAT

rem Get player names.
arexe30 arplyrs %2 /tag=name /ids=AR$PIDS /out=AR$NAMES
if errorlevel 1 goto STOPBAT

rem Get tournament seed ratings.
arexe30 arplyrs %2 /tag=rating /tag=sigma /ids=AR$PIDS /out=AR$TRATS
if errorlevel 1 goto STOPBAT

rem
rem Update ratings.
rem

rem Calculate seed ratings and sigmas for ratings update.
arexe30 arseeds AR$TRATS /base=%1 /out=AR$SEEDS
if errorlevel 1 goto STOPBAT

rem Calculate new ratings.
arexe30 aratings AR$GAMES AR$SEEDS /out=AR$NRATS
if errorlevel 1 goto STOPBAT

rem Create new base ratings file.
arexe30 arplyrs %1 AR$NAMES AR$NRATS /tag=name /tag=rating /tag=sigma /out=%3
if errorlevel 1 goto STOPBAT

rem
rem Write reports.
rem

rem Write ratings list in constant width font format.
arexe30 areportp AR$NAMES AR$NRATS /tag=rating /tag=winfraction /tag=name /out=RATSCW
if errorlevel 1 goto STOPBAT

rem Write ratings list with a tab before each field.
arexe30 areportp AR$NAMES AR$NRATS /tag=rating /tag=winfraction /tag=name /wp /out=RATSWP
if errorlevel 1 goto STOPBAT

rem Write ratings list in HTML.
arexe30 areportp AR$NAMES AR$NRATS /tag=rating /tag=winfraction /tag=name /html /out=RATSWEB
if errorlevel 1 goto STOPBAT
rename RATSWEB.TXT RATSWEB.HTM

rem Write individual game statistics.
arexe30 areportg AR$GAMES AR$NAMES AR$NRATS /html /out=GAMESTAT
if errorlevel 1 goto STOPBAT
rename GAMESTAT.TXT GAMESTAT.HTM

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
echo    %3.TDE - New base ratings file
echo    RATSCW.TXT   - Updated ratings list, assuming constant width font
echo    RATSWP.TXT   - Updated ratings list, with tabs for word processor
echo    RATSWEB.HTM  - Updated ratings list, for web browser
echo    GAMESTAT.HTM - Report showing each player's tournament games
echo Remember to e-mail %2.TDE to ratings@usgo.org for real ratings!

goto DONE

:STOPBAT
echo Script execution stopped due to error.

:DONE

