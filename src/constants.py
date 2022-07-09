from textformat import *
# Download Links for Drivers (Static)
STUDIO_DESKTOP_LINKS = {
    'DCH': ('https://international.download.nvidia.com/Windows/{driver_version}/{driver_version}-desktop-win10-win11-64bit-international-nsd-dch-whql.exe',
            'https://international.download.nvidia.com/Windows/{driver_version}/{driver_version}-desktop-win10-64bit-international-nsd-dch-whql.exe'),

    'STD': ('https://international.download.nvidia.com/Windows/{driver_version}/{driver_version}-desktop-win10-win11-64bit-international-nsd-whql.exe',
            'https://international.download.nvidia.com/Windows/{driver_version}/{driver_version}-desktop-win10-64bit-international-nsd-whql.exe'),
}
STUDIO_NOTEBOOK_LINKS = {
    'DCH': ('https://international.download.nvidia.com/Windows/{driver_version}/{driver_version}-notebook-win10-win11-64bit-international-nsd-dch-whql.exe',
            'https://international.download.nvidia.com/Windows/{driver_version}/{driver_version}-notebook-win10-64bit-international-nsd-dch-whql.exe'),

    'STD': ('https://international.download.nvidia.com/Windows/{driver_version}/{driver_version}-notebook-win10-win11-64bit-international-nsd-whql.exe',
            'https://international.download.nvidia.com/Windows/{driver_version}/{driver_version}-notebook-win10-64bit-international-nsd-whql.exe'),
}

GR_DESKTOP_LINKS = {
    'DCH': ('https://international.download.nvidia.com/Windows/{driver_version}/{driver_version}-desktop-win10-win11-64bit-international-dch-whql.exe',
            'https://international.download.nvidia.com/Windows/{driver_version}/{driver_version}-desktop-win10-64bit-international-dch-whql.exe'),

    'STD': ('https://international.download.nvidia.com/Windows/{driver_version}/{driver_version}-desktop-win10-win11-64bit-international-whql.exe',
            'https://international.download.nvidia.com/Windows/{driver_version}/{driver_version}-desktop-win10-64bit-international-whql.exe')
}

GR_NOTEBOOK_LINKS = {
    'DCH': ('https://international.download.nvidia.com/Windows/{driver_version}/{driver_version}-notebook-win10-win11-64bit-international-dch-whql.exe',
            'https://international.download.nvidia.com/Windows/{driver_version}/{driver_version}-notebook-win10-64bit-international-dch-whql.exe'),

    'STD': ('https://international.download.nvidia.com/Windows/{driver_version}/{driver_version}-notebook-win10-win11-64bit-international-whql.exe',
            'https://international.download.nvidia.com/Windows/{driver_version}/{driver_version}-notebook-win10-64bit-international-whql.exe')
}

QUADRO_LINKS = (
    'https://international.download.nvidia.com/Windows/Quadro_Certified/{driver_version}/{driver_version}-quadro-rtx-desktop-notebook-win10-win11-64bit-international-dch-whql.exe')


# API Link.
API_LINK = 'https://www.nvidia.com/Download/processFind.aspx?psid={psid}&pfid={pfid}&osid=57&lid=1&whql={whql}&ctk=0&dtcid={dtcid}'

# Base Driver Package Components.
BASE_COMPONENTS = ['Display.Driver',
                   'NVI2',
                   'EULA.txt',
                   'ListDevices.txt',
                   'setup.cfg',
                   'setup.exe']

# Setup
SETUP = ('<file name="${{EulaHtmlFile}}"/>',
         '<file name="${{PrivacyPolicyFile}}"/>',
         '<file name="${{FunctionalConsentFile}}"/>')

PRESENTATIONS = ('\t\t<string name="ProgressPresentationUrl"',
                 '\t\t<string name="ProgressPresentationSelectedPackageUrl"')

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

 NVDDL Docs/Wiki: {fg.lblue}https://github.com/Aetopia/NVIDIA-Driver-Downloader/wiki{eol}'''
