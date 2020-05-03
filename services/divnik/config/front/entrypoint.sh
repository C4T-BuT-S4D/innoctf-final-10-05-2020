#!/bin/sh

set -e

echo "[*] Setting up web support"
flutter channel beta
flutter upgrade
flutter config --enable-web

cd /app

echo "[*] Building"
flutter build web

echo "[*] Removing old files"
rm -rf /front/*

echo "[*] Copying files"
cp -r /app/build/web/* /front/

echo "[*] Done"
