@echo off
rem *********************************************************
rem AccelRat 3.0.1 - Copyright (c) 1995-1998 Paul G. Matthews
rem *********************************************************

rem
rem This script generates "true" ratings for a tournament simulation
rem based on the rating and sigma values in a player register file.
rem

rem Check arguments
if not X%1==X goto ARGS
if not exist REGISTER.TDE goto MISSING
goto READYGO

:MISSING
echo You should have the following file in your current directory:
echo   REGISTER.TDE - Registered players
echo.

:ARGS
echo No command line arguments are expected.
echo.
goto STOPBAT

:READYGO

rem Erase any previous effort and temporary files
if exist TRUERATS.TDE erase TRUERATS.TDE
if exist *.LOG erase *.LOG
if exist AR$*.* erase AR$*.*

echo Processing ...

rem Check format of player register.
arexe30 archeck REGISTER /out=AR$CHK
if errorlevel 1 goto STOPBAT

rem Calculate seed rating and sigma for each registered player.
arexe30 arseeds REGISTER /out=AR$SEEDS
if errorlevel 1 goto STOPBAT

rem Draw true ratings from seed rating distributions.
arexe30 arsimtr AR$SEEDS /out=TRUERATS
if errorlevel 1 goto STOPBAT

rem Erase temporary files.
erase *.LOG
erase AR$*.*

echo Look for the following file in your current directory:
echo    TRUERATS.TDE - True ratings for simulation

goto DONE

:STOPBAT
echo Script execution stopped due to error.

:DONE

