set application_data=--windows-product-name="NVIDIA Driver Downloader" --windows-file-version=1.0.0.0 --windows-product-version=1.0.0.0 --windows-file-description="NVIDIA Driver Downloader"
nuitka --follow-imports --onefile --standalone --remove-output %Application_data% --run nvddl.py
