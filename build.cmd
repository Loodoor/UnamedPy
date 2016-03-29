cd src
echo Starting build

echo -------------------------------

C:\Python34\Scripts\cxfreeze -s -O --target-dir=..\build main.py
REM --icon=ICON

echo -------------------------------

echo Build finished !

cd ..