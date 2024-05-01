@echo off
setlocal

echo --------------------------------------------------------
echo +      Starting Python Flask Web application           +
echo --------------------------------------------------------

@REM Check if Python is installed
where python >nul 2>&1 || (
    call :exit_error "Python is not installed on this machine. Please install Python and try again."
)

@REM Change directory to app folder
cd app

@REM Check if virtual environment exists
IF EXIST venv (
    call :info "Virtual environment exists."
) ELSE (
    call :info "Virtual environment does not exist. Creating virtual environment."
    python -m venv venv
)

@REM Activate virtual environment
call :info "Activating Virtual environment."
call venv\Scripts\activate.bat || (
    call :exit_error "Failed to activate virtual environment. Please make sure the virtual environment exists and try again."
)


@REM Install dependencies
call :info "Installing dependencies."
pip install -r requirements.txt || (
    call :exit_error "Failed to install dependencies. Please make sure requirements.txt exists and try again."
)

@REM Check if a Python script named "run.py" exists in the current directory.
@REM If it does, the script is executed using the Python interpreter. 
@REM If it doesn't, an error message is displayed and the script exits with an error code.

set RUN_APP_SCRIPT="run.py"

IF EXIST %RUN_APP_SCRIPT% (
    call :info "Running %RUN_APP_SCRIPT% script."
    python %RUN_APP_SCRIPT%
) ELSE (
    call :exit_error "The script %RUN_APP_SCRIPT% does not exist."
)

call :exit_success
endlocal
GOTO :EOF


@REM Exit labels

:exit_success
echo --------------------------------------------------------
echo +     Python Flask Web application stopped running     +
echo --------------------------------------------------------
exit /b 0

:exit_error
call :error %1
exit /b 1

@REM Messeges labels

:info
echo INFO: %1
GOTO :EOF

:warning
echo WARNING: %1
GOTO :EOF

:error
echo ERROR: %1
GOTO :EOF





