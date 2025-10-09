@echo off
chcp 65001 >nul
echo ========================================
echo TwitchDropsMiner Android - GitHub Setup
echo ========================================
echo.

git --version >nul 2>&1
if errorlevel 1 (
    echo Git nie je nainstalovany!
    echo Stiahni: https://git-scm.com/downloads
    pause
    exit /b 1
)

echo Git OK
echo.

set /p username="GitHub username: "
set /p reponame="Nazov repozitara: "

echo.
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/%username%/%reponame%.git
git branch -M main
git push -u origin main

echo.
echo HOTOVO!
echo Chod na: https://github.com/%username%/%reponame%
echo Settings - Actions - General - Allow all actions - Save
echo.
pause