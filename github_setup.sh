#!/bin/bash
echo "TwitchDropsMiner Android - GitHub Setup"
echo ""

if ! command -v git &> /dev/null; then
    echo "Git nie je nainstalovany!"
    exit 1
fi

echo "Git OK"
echo ""

read -p "GitHub username: " username
read -p "Nazov repozitara: " reponame

echo ""
git init
git add .
git commit -m "Initial commit"
git remote add origin "https://github.com/$username/$reponame.git"
git branch -M main
git push -u origin main

echo ""
echo "HOTOVO!"
echo "Chod na: https://github.com/$username/$reponame"
echo "Settings - Actions - General - Allow all actions - Save"