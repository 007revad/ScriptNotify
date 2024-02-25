#!/bin/bash
# Filename: build_spk.sh - coded in utf-8

#                ScriptNotify
#        Copyright (C) 2022 by 007revad 

MY_PATH="$(dirname -- "${BASH_SOURCE[0]}")"
echo "$MY_PATH"
cd "$MY_PATH"

# Set Package Version
version="1.0.0-0001"

# Set Package Name
package="ScriptNotify"

# Set folder and file permissions
chmod -R 755 ./package
chmod 700 ./package/ui/modules/synowebapi
chmod -R 777 ./conf
chmod -R 777 ./scripts
chmod -R 777 ./WIZARD_UIFILES
chmod 777 ./CHANGELOG
chmod 777 ./INFO
chmod 777 ./LICENSE
chmod 777 ./PACKAGE_ICON*

# Build SPK
echo "Building SPK"
tar -C ./package/ -czf ./package.tgz .
chmod 755 ./package.tgz
#tar --exclude="package/*" --exclude="build_spk.sh" --exclude=".git/*" --exclude=".gitignore/*" --exclude="README.md" --exclude="README_en.md" -cvf ${package}_${version}.spk *
tar --exclude="package" --exclude="build_spk.sh" --exclude="CHANGE.LOG" --exclude=".git/*" --exclude=".gitignore/*" --exclude="README.md" --exclude="README_en.md" -cvf "${package}_${version}.spk" *
rm -f package.tgz
