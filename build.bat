: NVIDIA Driver Downloader Build Script
@echo off
set version=1.4.0.0
mkdir build
cd src
nuitka --follow-imports --assume-yes-for-downloads --warn-unusual-code --warn-implicit-exceptions --include-plugin-files="functions.py" --include-plugin-files="helpers.py" --include-plugin-files="textformat.py" --include-plugin-files="constants.py" --include-plugin-files="utils.py" --onefile --standalone --remove-output --windows-company-name=Aetopia --windows-product-name="NVIDIA Driver Downloader" --windows-file-version="%version%" --windows-product-version="%version%" --windows-file-description="NVIDIA Driver Downloader" --run -o "..\build\nvddl.exe" main.py 
