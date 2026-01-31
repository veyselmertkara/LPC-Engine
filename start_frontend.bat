@echo off
echo ========================================
echo   LPC Engine - Frontend Starter
echo ========================================
echo.

cd frontend

echo Checking Node.js installation...
node --version
if errorlevel 1 (
    echo ERROR: Node.js is not installed or not in PATH!
    echo Please install Node.js 16+ from https://nodejs.org/
    pause
    exit /b 1
)

echo.
echo Checking dependencies...
if not exist "node_modules\" (
    echo Installing dependencies...
    npm install
)

echo.
echo Starting frontend development server...
echo Frontend will run at: http://localhost:5173
echo Press Ctrl+C to stop the server
echo.

npm run dev
