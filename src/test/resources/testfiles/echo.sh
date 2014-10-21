#!/bin/sh
echo "Hi $1"
if [ ! -z "$2" ]
    then
        echo "Exiting with $2"
        exit $2
fi
echo "Exiting"