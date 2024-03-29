from plugins.textformat import eol, fg

# Help
HELP_ARGUMENTS = '''--list, -ls                        │ Show all available driver versions.
--download, -dl <Driver Version>   │ Download the latest driver or a specified driver version.
--extract, -e <Driver File>        │ Extract the specified driver package.
--update, -u                       │ Check if the currently installed NVIDIA driver is outdated or not.'''

HELP_DRIVER_OPTIONS = '''--studio, -stu                     │ Set the driver type to Studio.
--standard, -std                   │ Set the driver type to Standard.
--full, -f                         │ Sets the driver package type to Full.
--setup, -s                        │ Run the extracted driver package setup.
--components, -c [Components ...]  │ Select which components to include in an extracted driver package.'''

HELP_OPTIONS = '''--output, -o <Directory>           │ Specify the output directory.
--flags [Flags ...]                │ Pass flags to NVDDL.'''

PROGRAM_DESCRIPTION = f''' 
 {fg.lgreen}┌──────────────────────────┐ 
 │@ NVIDIA Driver Downloader│
 └──────────────────────────┘{eol}

 A tool that allows you to download NVIDIA Game Ready and Studio drivers via the command-line. Made with Python!

 GitHub Repository: {fg.lblue}https://github.com/Aetopia/NVIDIA-Driver-Downloader{eol}

 NVDDL Docs/Wiki: {fg.lblue}https://github.com/Aetopia/NVIDIA-Driver-Downloader/wiki{eol}
'''
