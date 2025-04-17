@echo off
title Assistant Culinaire IA
echo.
echo ================================
echo     🍽️ Assistant Culinaire IA
echo ================================
echo.
echo Que veux-tu lancer ?
echo 1. Assistant en ligne de commande (PROJETV2.py)
echo 2. Interface graphique (interface2.py)
echo.

set /p choix=Fais ton choix (1 ou 2) : 

echo.
echo === Activation de l’environnement virtuel ===
call venv\Scripts\activate.bat

if "%choix%"=="1" (
    echo === Lancement du bot en terminal ===
    python PROJETV2.py
) else if "%choix%"=="2" (
    echo === Lancement de l'interface graphique ===
    python interface2.py
) else (
    echo Choix invalide. Relance le script et tape 1 ou 2.
)

pause
