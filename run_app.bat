@echo off
:: Set up the backend and frontend directories
SET BACKEND_DIR=.
SET FRONTEND_DIR=frontend

:: Navigate to the backend directory and install Python dependencies
echo Installing backend dependencies...
cd %BACKEND_DIR%
pip install -r requirements.txt

:: Start the Flask server
echo Starting the backend server...
start cmd /k "python run.py"

:: Navigate to the frontend directory and install Node.js dependencies
echo Installing frontend dependencies...
cd ..\%FRONTEND_DIR%
npm install

:: Start the React server
echo Starting the frontend server...
start cmd /k "npm run start"

:: Return to the root directory
cd ..
echo Both servers are running. Press any key to exit this script.
pause