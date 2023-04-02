@echo off
echo Powering on the Valdevian Translator...
pause
py -m pip install transformers
py -m pip install torch
py -m pip install Flask

set current_dir=%cd%

echo  _______________________________________
echo ^| Valdevian Translator has loaded!   ^|
echo ^| In your browser type               ^|
echo ^| http://localhost:5000/             ^|
echo ^|____________________________________^|
color 1F
call python %current_dir%\py\backend.py
timeout /t 5 /nobreak > NUL

pause
