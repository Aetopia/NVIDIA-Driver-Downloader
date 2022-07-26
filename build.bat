: NVIDIA Driver Downloader Build Script
@echo off
set version=1.4.0.0
mkdir build
cd src
nuitka --follow-imports --assume-yes-for-downloads --warn-unusual-code --warn-implicit-exceptions --include-plugin-files="core/functions.py" --include-plugin-files="plugins/files.py" --include-plugin-files="data/strings.py" --include-plugin-files="plugins/textformat.py" --include-plugin-files="data/constants.py" --include-plugin-files="plugins/utils.py" --include-plugin-files="core/cli.py" --onefile --standalone --remove-output --windows-company-name=Aetopia --windows-product-name="NVIDIA Driver Downloader" --windows-file-version="%version%" --windows-product-version="%version%" --windows-file-description="NVIDIA Driver Downloader" --run -o "..\build\nvddl.exe" main.py 
