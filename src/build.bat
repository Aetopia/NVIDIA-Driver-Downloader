: NVIDIA Driver Downloader Build Script
@echo off
set version=1.3.0.0
nuitka --follow-imports --include-plugin-files="functions.py" --include-plugin-files="constants.py" --include-plugin-files="utils.py" --onefile --standalone --remove-output --windows-company-name=Aetopia --windows-product-name="NVIDIA Driver Downloader" --windows-file-version="%version%" --windows-product-version="%version%" --windows-file-description="NVIDIA Driver Downloader" --run -o nvddl.exe main.py 
