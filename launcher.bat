REM launcher du jeu
cd src/
py -3.4 main.py "err_log.log" 2>&1
echo "Si le jeu se coupe brutalement et que vous pensez que cela est dû à un bug,"
echo "je vous serais reconnaissant de m'envoyer le contenu du fichier qui va s'ouvrir"
notepad "err_log.log"
cd ..
pause
