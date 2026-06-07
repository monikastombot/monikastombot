@echo off
cd /d C:\Users\Anastasia\Desktop\mybot
echo ===== Git Status =====
git status
echo.
echo ===== Adding files =====
git add .
echo.
echo ===== Git Status after add =====
git status
echo.
echo ===== Creating commit =====
git commit -m "Initial commit - Medical Platform"
echo.
echo Done!
pause
