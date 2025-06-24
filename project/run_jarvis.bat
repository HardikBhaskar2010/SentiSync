@echo off
echo Starting Jarvis AI Assistant...
echo.
echo Choose your mode:
echo 1. Voice Mode (Default)
echo 2. Text Mode
echo 3. GUI Mode
echo.
set /p choice="Enter your choice (1-3): "

if "%choice%"=="1" (
    echo Starting Voice Mode...
    python assistant.py
) else if "%choice%"=="2" (
    echo Starting Text Mode...
    python assistant.py --text
) else if "%choice%"=="3" (
    echo Starting GUI Mode...
    python gui_assistant.py
) else (
    echo Invalid choice. Starting Voice Mode...
    python assistant.py
)

pause