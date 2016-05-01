# launcher du jeu
cd src/
python3 main.py "err_log.log" 2>&1
echo "Si le jeu se coupe brutalement et que vous pensez que cela est dû à un bug,"
echo "je vous serais reconnaissant de m'envoyer le contenu du fichier qui va s'ouvrir"
gedit "err_log.log"
cd ..
read -n1 -r -p "Appuyez sur une touche pour terminer le programme ..." key
