# NVIDIA Driver Downloader
Allows you to download NVIDIA Game Ready and Studio drivers via the command-line. Made with 🐍 Python!

# Usage:
1. `--download <Driver Version>` | Download a specified driver version.     
`--download` | Download the latest driver.
2. `--list` | Return a list of driver versions.
3. `--unpack <Driver File>` | Unpack only the display driver from a driver package.
4. `--studio` | Set the driver type to Studio. (Default: Game Ready)
5. `--standard` | Set the driver type to Standard. (Default: DCH)
5. `--dir <Directory>` | Specify the output directory.
6. `--update` | Check if the installed NVIDIA driver is outdated or not.

# Releases
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
### 1. NVIDIA's Advanced Driver Search & Driver Package Unpacking: [NVIDIA-Update](https://github.com/lord-carlos/nvidia-update)
### 2. NVIDIA API: [EnvyUpdate](https://github.com/fyr77/EnvyUpdate/wiki/Nvidia-API)
