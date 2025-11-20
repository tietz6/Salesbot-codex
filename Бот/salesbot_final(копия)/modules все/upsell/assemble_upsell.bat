
@echo off
setlocal ENABLEDELAYEDEXPANSION
set BASEDIR=%~1
set ZIPSDIR=%~2
set FLAG=%~3
if "%BASEDIR%"=="" set BASEDIR=C:\Users\User\Desktop\salesbot_final\api\modules
if "%ZIPSDIR%"=="" set ZIPSDIR=.
echo [+] BaseDir: %BASEDIR%
echo [+] ZipsDir: %ZIPSDIR%
if "%FLAG%"=="--dry-run" (
  powershell -ExecutionPolicy Bypass -File "%~dp0assemble_upsell.ps1" -BaseDir "%BASEDIR%" -ZipsDir "%ZIPSDIR%" -DryRun
) else (
  powershell -ExecutionPolicy Bypass -File "%~dp0assemble_upsell.ps1" -BaseDir "%BASEDIR%" -ZipsDir "%ZIPSDIR%"
)
endlocal
