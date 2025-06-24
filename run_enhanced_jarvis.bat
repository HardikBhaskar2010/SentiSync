@echo off
echo Starting Enhanced Free AI Jarvis Assistant...
echo.
echo Choose your mode:
echo 1. Voice Mode (Default)
echo 2. Text Mode  
echo 3. Enhanced GUI Mode
echo.
set /p choice="Enter your choice (1-3): "

if "%choice%"=="1" (
    echo Starting Enhanced Voice Mode...
    python free_ai_assistant.py
) else if "%choice%"=="2" (
    echo Starting Enhanced Text Mode...
    python free_ai_assistant.py --text
) else if "%choice%"=="3" (
    echo Starting Enhanced GUI Mode...
    python enhanced_gui.py
) else (
    echo Invalid choice. Starting Enhanced Voice Mode...
    python free_ai_assistant.py
)

pause