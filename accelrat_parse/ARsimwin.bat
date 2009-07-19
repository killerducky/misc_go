@echo off
rem *********************************************************
rem AccelRat 3.0.1 - Copyright (c) 1995-1999 Paul G. Matthews
rem *********************************************************

rem
rem This script simulates winners for a tournament round.
rem

rem Check required input
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
if not exist TRUERATS.TDE goto MISSING
if not exist %1.TDE goto MISSING
goto READYGO

:MISSING
echo You should have the following files in your current directory:
echo    TRUERATS.TDE - True ratings of registered players
echo    %1.TDE        - Paired games for round %1
echo.

:ARGS
echo You must provide one command line argument:
echo    (1) round number (i.e., 1, 2, 3, ...)
echo For example,
echo    %0 1
echo.
goto STOPBAT

:READYGO

rem Erase any temporary files
if exist *.LOG erase *.LOG
if exist AR$*.* erase AR$*.*

echo Processing ...

rem Simulate game winners based on true rating difference probabilities.
arexe30 arsimgw %1 TRUERATS /out=AR$RSLTS
if errorlevel 1 goto STOPBAT

rem Replace game records for this round.
copy AR$RSLTS.TDE %1.TDE /b
if errorlevel 1 goto STOPBAT

echo %1.TDE has been replaced with simulated game results.

rem Erase temporary files
erase *.LOG
erase AR$*.*

goto DONE

:STOPBAT
echo Script execution stopped due to error.

:DONE

