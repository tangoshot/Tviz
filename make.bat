rm -r -f ./build
rm -r -f ./dist
pause

python setup.py build

set pythonpath=%pythonpath%;./src

echo %pythonpath%

python C:/CodeBench/xlib/python/pyinstaller-2.0/pyinstaller.py --noupx --onefile --buildpath=build/dist run.py 

cp -r -u resources ./dist/resources
cp -r -u user ./dist/user
