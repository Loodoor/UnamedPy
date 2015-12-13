REM launcher du serveur
cd src/
color 0f
py -3.4 serveur.py "serv_err_log.log" REM 2>&1
REM notepad "serv_err_log.log"
cd ..
pause