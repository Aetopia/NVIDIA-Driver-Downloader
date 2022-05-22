# NVIDIA Driver Downloader
Allows you to download NVIDIA Game Ready and Studio drivers via the command-line. Made with 🐍 Python!                     
This tool is aimed at Windows 10+ and modern NVIDIA GPUs.
# Usage:
1. `--download <Driver Version>` | Download a specified driver version.     
`--download` | Download the latest driver.
2. `--list` | Return a list of driver versions.
3. `--extract <Driver File>` | Extract the specified driver package.
4. `--studio` | Set the driver type to Studio. (Default: Game Ready)
5. `--standard` | Set the driver type to Standard. (Default: DCH)
6. `--output <Directory>` | Specify the output directory.    
`--output` | Set the output directory to the current working directory.
7. `--update` | Check if the currently installed NVIDIA driver is outdated or not.
8. `--full` | Sets the driver package type to Full.
9. `--components [Components]` | Specify which components to include when extracting a driver package.

# Wiki
### Check out NVDDL's Documentation/Wiki: [Documentation/Wiki](https://github.com/Aetopia/NVIDIA-Driver-Downloader/wiki)

# Releases
**Install via Scoop**
```ps
scoop install https://raw.githubusercontent.com/couleur-tweak-tips/utils/main/bucket/nvddl.json
```
**Find pre-compiled binaries here:**             
[GitHub Releases](https://github.com/Aetopia/NVIDIA-Driver-Downloader/releases)

# Requirements
```
pip install wmi
```

# Build
1. Install the following using `pip`:
    ```
    pip install nuitka zstandard
    ```
2. Go into the `src` folder and run `build.bat`.

# Sources
### 1. NVIDIA's Advanced Driver Search & Driver Package Extraction: [NVIDIA-Update](https://github.com/lord-carlos/nvidia-update)
### 2. NVIDIA API: [EnvyUpdate](https://github.com/fyr77/EnvyUpdate/wiki/Nvidia-API)
