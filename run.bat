@echo off
echo === Activation de l'environnement virtuel ===
call venv\Scripts\activate.bat

echo.
echo === Lancement de l'assistant culinaire ===
python PROJETV2.py

echo.
pause
