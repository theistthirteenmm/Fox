@echo off
setlocal

cd /d "%~dp0\.."

set "NGINX_CONF=%CD%\config\nginx\robah.conf"
set "NGINX_ROOT=%CD%"
set "NGINX_LOG_DIR=%CD%\logs\nginx"

if not exist "%NGINX_CONF%" (
    echo Nginx config not found: %NGINX_CONF%
    exit /b 1
)

where nginx >nul 2>&1
if %errorlevel% neq 0 (
    echo Nginx not found in PATH. Install nginx and add it to PATH.
    exit /b 1
)

if not exist "%NGINX_LOG_DIR%" (
    mkdir "%NGINX_LOG_DIR%"
)

nginx -s quit -c "%NGINX_CONF%" -p "%NGINX_ROOT%" >nul 2>&1
nginx -c "%NGINX_CONF%" -p "%NGINX_ROOT%"

endlocal
