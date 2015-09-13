REM launcher du jeu
cd src/
color 0f
py -3.4 main.py "errors/err_log.log" REM 2>&1
REM notepad "errors/err_log.log"
cd ..