# NVIDIA Driver Downloader
Allows you to download NVIDIA Game Ready and Studio drivers via the command line. Made with 🐍 Python!

# Usage:
1. `-download <Driver Version>`: Download the latest driver or a specified driver version.
2. `-list`: Return a list of driver versions. Combine with `-type` to filter out Game Ready or Studio drivers.
3. `-unpack <Driver File>`: Unpack only the display driver from a driver package.
4. `type <GR/Studio>`: Specify the type of driver, Game Ready or Studio.
5. `-dir`: Specify the directory where the driver should be downloaded. 

# Releases
**Find pre-compiled binaries here:**             
[GitHub Releases](https://github.com/Aetopia/NVIDIA-Driver-Downloader/releases)         

# Build
1. Install the following using `pip`:
```
pip install nuitka zstandard
```
2. Run `build.bat`.

# Sources
#### This project is uses some handy information on NVIDIA's Advanced Driver Search & Driver Package unpacking from [NVIDIA-Update](https://github.com/lord-carlos/nvidia-update).
