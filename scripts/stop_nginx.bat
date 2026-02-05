@echo off
setlocal

cd /d "%~dp0\.."

set "NGINX_CONF=%CD%\config\nginx\robah.conf"
set "NGINX_ROOT=%CD%"

where nginx >nul 2>&1
if %errorlevel% neq 0 (
    echo Nginx not found in PATH.
    exit /b 1
)

nginx -s quit -c "%NGINX_CONF%" -p "%NGINX_ROOT%"

endlocal
