@echo off
cd /d "%~dp0"
echo Installing/updating required Python packages...
py -m pip install -r requirements.txt
if errorlevel 1 goto failed
echo Downloading HiroSaito04 public GitHub contribution calendar...
py scripts/render_contributions.py --fetch
if errorlevel 1 goto failed
echo.
echo Success! Open preview.html to view the REAL calendar with slower Brio animation.
pause
exit /b 0
:failed
echo.
echo Failed. No fake data will be presented as real. Check your internet connection, then retry.
pause
exit /b 1
