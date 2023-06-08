if exist .\dist rd/s/q .\dist 
if exist .\build rd/s/q .\build
call conda activate noelle-calculator-env
pyinstaller main_func.py -w -i "favicon.ico" -n "Noelle_Calculator"
copy .\readme.txt .\dist\Noelle_Calculator\
copy .\background*.png .\dist\Noelle_Calculator\
copy .\favicon.ico .\dist\Noelle_Calculator\
rd/s/q .\dist\Noelle_Calculator\mpl-data
pause