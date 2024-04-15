#!/bin/bash

system="$1"

if [ $system == "linux" ]; then
  command="-n encrypt --onedir --windowed --icon app/static/icon.icns app/main.py"
elif [ $system == "windows" ]; then
  command="-n encrypt --onedir --windowed --icon app/static/icon.ico app/main.py"
else
  echo "You must specify operating system (windows, linux)"
  exit 1
fi

rm -rf encrypt.spec
rm -rf build
rm -rf dist


pyinstaller $command

if [ $? -eq 0 ]; then
    echo "Build successful!"
else
    echo "Build failed!"
fi
