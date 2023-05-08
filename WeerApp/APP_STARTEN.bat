@echo off
title App Starter
color c                                                                                             
cls
if exist node_modules\ (
echo ==========================================
echo             Starten van de APP
echo ==========================================
npx expo start
) else (
echo ==========================================
echo             Installeren
echo ==========================================
npm install
APP_STARTEN.bat
exit
)