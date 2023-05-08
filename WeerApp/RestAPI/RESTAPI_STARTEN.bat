@echo off
title RestAPI Starter
color c                                                                                             
cls
echo ==========================================
echo             Starten van de RESTAPI
echo ==========================================
if exist env\ (
cd env/Scripts
activate
cd..
cd..
$env:FLASK_APP = "app.py"
SET FLASK_APP=app.py
SET FLASK_DEBUG=1
start http://127.0.0.1:5000/forecast
flask run
) else (
echo ==========================================
echo                 ERROR
echo ==========================================
)