# NVIDIA Driver Downloader
Allows you to download NVIDIA Game Ready and Studio drivers via the command line. Made with 🐍 Python!

# Usage:
1. `-download <Driver Version>`: Download the latest driver or provide a driver version to download.
2. `type <GR/Studio>`: Specify the type of driver, Game Ready or Studio.
3. `-list`: Return a list of driver version. Combine with `-type` to filter out Game Ready or Studio drivers.
4. `-dir`: Specify the directory where the driver should be downloaded. 

# Build
1. Install the following using `pip`:
```
pip install nuitka zstandard
```
2. Run `build.bat`.

# Sources
#### This project is uses some handy information on NVIDIA's Advanced Driver Search from [NVIDIA-Update](https://github.com/lord-carlos/nvidia-update).
