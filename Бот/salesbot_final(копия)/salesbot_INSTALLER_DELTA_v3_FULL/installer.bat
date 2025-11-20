@echo off
setlocal EnableExtensions EnableDelayedExpansion

rem --- Paths ---
set "HERE=%~dp0"
pushd "%HERE%" >NUL
cd /d "%HERE%"
set "ROOT=%CD%"
set "PARTS=%ROOT%\..\parts"
set "AUTOB=%ROOT%\..\autobuilder_module"

echo [1/4] Checking folders...
if not exist "%PARTS%" (
  echo ERROR: parts\ folder not found at "%PARTS%".
  echo Put all salesbot_PART_XX_*.zip into parts\ and run again.
  pause & exit /b 1
)
if not exist "%AUTOB%\autobuilder\__init__.py" (
  echo ERROR: autobuilder_module\autobuilder not found at "%AUTOB%".
  echo Make sure folder "autobuilder_module\autobuilder" exists.
  pause & exit /b 1
)

echo [2/4] Selecting Python...
where py >NUL 2>NUL && (set "PYEXE=py -3") || (set "PYEXE=python")
%PYEXE% -V || (echo ERROR: Python not found in PATH & pause & exit /b 1)

echo [3/4] Creating virtual env (.venv)...
if not exist "%ROOT%\.venv\Scripts\python.exe" (
  %PYEXE% -m venv "%ROOT%\.venv" || (echo ERROR: venv create failed & pause & exit /b 1)
)

set "VENV=%ROOT%\.venv\Scripts\python.exe"
echo [3/4] Installing deps...
"%VENV%" -m pip install --upgrade pip setuptools wheel >NUL
if exist "%ROOT%\_installer\requirements.txt" (
  "%VENV%" -m pip install -r "%ROOT%\_installer\requirements.txt"
) else (
  "%VENV%" -m pip install fastapi uvicorn jinja2 colorama httpx
)

echo [4/4] Applying parts with autobuilder...
set "PYTHONPATH=%AUTOB%;%PYTHONPATH%"
"%VENV%" -m autobuilder.apply_all "%PARTS%" || (echo ERROR: autobuilder failed & pause & exit /b 1)

echo.
echo [OK] All parts applied successfully.
echo To start API now, run: start_api.bat
echo.
pause
popd >NUL
endlocal
