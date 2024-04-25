
set n=0
:abc
set /a n+=1
py bot.py
CHOICE /T 3 /C ync /CS /D y /n 
if %n%==99999999999999 exit
goto abc
pause