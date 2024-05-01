
@echo off
setlocal

set MONGO_HOME=C:\Program Files\MongoDB\Server\7.0\bin
set MONGO_EXE=%MONGO_HOME%\mongod.exe
set DATABSE_PATH=%cd%\data\db

echo --------------------------------------------------------
echo +             Starting Mongo Database                  +
echo --------------------------------------------------------

call :info "[MONGO_HOME] %MONGO_HOME%"
call :info "[MONGO_EXE] %MONGO_EXE%"
call :info "[DATABSE_PATH] %DATABSE_PATH%"

@REM Check if Mongo is installed
IF EXIST "%MONGO_HOME%" (
    call :info "MongoDB is installed."
) ELSE (
    call :exit_error "MongoDB is not installed. Please install it and try again."
)

call "%MONGO_EXE%" --dbpath "%DATABSE_PATH%" || (
    call :exit_error "Failed to start the databse."
)





call :exit_success
endlocal
GOTO :EOF


@REM Exit labels

:exit_success
echo --------------------------------------------------------
echo +          Mongo Database stopped running              +
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
echo ERROR: %~1
GOTO :EOF
