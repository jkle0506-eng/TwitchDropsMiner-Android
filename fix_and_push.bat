@echo off
echo Nastavujem Git...

git config --global user.email "jkle0506@gmail.com"
git config --global user.name "jkle0506-eng"

echo Nahráváam na GitHub...
git add .
git commit -m "Initial commit - TwitchDropsMiner Android"
git branch -M main
git push -u origin main

echo.
echo HOTOVO!
echo Chod na: https://github.com/jkle0506-eng/TwitchDropsMiner-Android
echo Settings - Actions - General - Allow all actions - Save
pause