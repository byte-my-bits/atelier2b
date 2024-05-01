#!/bin/bash

MONGO_HOME="/usr/local/mongodb"
MONGO_EXE="$MONGO_HOME/bin/mongod"
DATABASE_PATH="data/db"

echo "--------------------------------------------------------"
echo "+             Starting Mongo Database                  +"
echo "--------------------------------------------------------"

echo "[MONGO_HOME] $MONGO_HOME"
echo "[MONGO_EXE] $MONGO_EXE"
echo "[DATABASE_PATH] $DATABASE_PATH"

# Check if Mongo is installed
if [ -d "$MONGO_HOME" ]
then
    echo "MongoDB is installed."
else
    echo "MongoDB is not installed. Installing MongoDB..."
    sudo apt update
    sudo apt install -y mongodb
    echo "MongoDB installation complete."
fi

# Start MongoDB
"$MONGO_EXE" --dbpath "$DATABASE_PATH" || {
    echo "Failed to start the database."
    exit 1
}

echo "--------------------------------------------------------"
echo "+          Mongo Database stopped running              +"
echo "--------------------------------------------------------"