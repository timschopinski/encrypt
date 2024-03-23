#!/bin/bash

rm -rf encrypt.spec
rm -rf build
rm -rf dist


pyinstaller -n encrypt --icon app/static/icon.icns --onedir app/main.py

if [ $? -eq 0 ]; then
    echo "Build successful!"
else
    echo "Build failed!"
fi
