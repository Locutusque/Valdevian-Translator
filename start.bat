@echo off
echo Powering on the Valdevian Translator...
pause
for /f "tokens=*" %%a in ('python -c "import os, sys; print(os.path.dirname(sys.executable))"') do set PY=%%a
"%PY%\python.exe" -m pip install transformers
"%PY%\python.exe" -m pip install torch
"%PY%\python.exe" -m pip install Flask

set current_dir=%cd%

echo  _______________________________________
echo ^| Valdevian Translator has loaded!   ^|
echo ^| In your browser type               ^|
echo ^| http://localhost:5000/             ^|
echo ^|____________________________________^|
color 1F
call "%PY%\python.exe" %current_dir%\py\backend.py
timeout /t 5 /nobreak > NUL

pause
