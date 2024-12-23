@echo off
REM This is a batch file to run the Flask application

REM Navigate to the directory where your Flask app is located
cd /d "C:\path\to\your\flask\app"  REM Replace with the actual path to your app

REM Install dependencies from requirements.txt
echo Installing dependencies from requirements.txt...
pip install -r requirements.txt

REM Run the Flask application
echo Running Flask app...
python app.py

REM Pause the command window to keep it open after execution
pause
