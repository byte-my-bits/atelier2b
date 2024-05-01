#!/bin/bash

echo "--------------------------------------------------------"
echo "+      Starting Python Flask Web application           +"
echo "--------------------------------------------------------"

# Check if Python is installed
if ! command -v python &> /dev/null
then
    echo "Python is not installed on this machine. Please install Python and try again."
    exit 1
fi

# Change directory to app folder
cd app

# Check if virtual environment exists
if [ -d "venv" ]
then
    echo "Virtual environment exists."
else
    echo "Virtual environment does not exist. Creating virtual environment."
    python -m venv venv
fi

# Activate virtual environment
echo "Activating Virtual environment."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies."
pip install -r requirements.txt

# Check if a Python script named "run.py" exists in the current directory.
# If it does, the script is executed using the Python interpreter. 
# If it doesn't, an error message is displayed and the script exits with an error code.

RUN_APP_SCRIPT="run.py"

if [ -f "$RUN_APP_SCRIPT" ]
then
    echo "Running $RUN_APP_SCRIPT script."
    python $RUN_APP_SCRIPT
else
    echo "The script $RUN_APP_SCRIPT does not exist."
    exit 1
fi

echo "--------------------------------------------------------"
echo "+     Python Flask Web application stopped running     +"
echo "--------------------------------------------------------"