# NVIDIA Driver Downloader made by Aetopia.
# GitHub Repository: https://github.com/Aetopia/NVIDIA-Driver-Downloader
# Discord: https://dsc.gg/CTT
# Under the MIT License: https://github.com/Aetopia/NVIDIA-Driver-Downloader/blob/main/LICENSE.md

# Modules
from os import getcwd, path
from urllib.request import urlopen, HTTPError
from pathlib import Path
from argparse import ArgumentParser
from codecs import decode
from fnmatch import fnmatch
from subprocess import run
from sys import argv

# Functions

# Get NVIDIA Driver Versions.
def get_driver_versions(studio_drivers = False):
    link = 'https://www.nvidia.com/Download/processFind.aspx?psid=101&pfid=845&osid=57&lid=1&whql=1&ctk=0&dtcid=1'
    with urlopen(link) as file:
        file = file.readlines()  
    gr_driver_versions = ()     
    for line in file:
        line = decode(line, 'UTF-8').strip()
        if fnmatch(line, '<td class="gridItem">*.*</td>'):
            version = line.split('>')[1].split('<')[0]
            if version != '':
                gr_driver_versions += version,
    if studio_drivers:
        studio_driver_versions = ()
        for version in gr_driver_versions:
            try:
                if urlopen(f'https://international.download.nvidia.com/Windows/{version}/{version}-desktop-win10-win11-64bit-international-nsd-dch-whql.exe').getcode() == 200: 
                    studio_driver_versions += version,
            except HTTPError:
                pass    
        return(studio_driver_versions)                           
    else:
        return(gr_driver_versions)            

# Download an NVIDIA Driver Package.
def download(driver_version = None, studio_drivers = False, dir = getcwd()):
    if driver_version is None:
        driver_versions = get_driver_versions(studio_drivers = studio_drivers)
    else:
        driver_versions = (driver_version,)  
    if studio_drivers is True:
        prefix = 'Studio'
        driver_link = 'https://international.download.nvidia.com/Windows/{driver_version}/{driver_version}-desktop-win10-win11-64bit-international-nsd-dch-whql.exe' 
    elif studio_drivers is False:
        prefix = 'Game Ready'
        driver_link = 'https://international.download.nvidia.com/Windows/{driver_version}/{driver_version}-desktop-win10-win11-64bit-international-dch-whql.exe'        
    print('Checking Download...')
    try:
        if urlopen(f'{driver_link}'.format(driver_version = driver_versions[0])).getcode() == 200:
            print('Version is valid, now downloading NVIDIA Driver...')
            run(f'curl.exe -# "{driver_link}" -o "{dir}/{prefix} - {driver_versions[0]}.exe"'.format(driver_version = driver_versions[0]))
    except:
        print("Version isn't valid...")  

# Unpack only the Display Driver from an NVIDIA Driver Package.
def unpack(driver_file, dir = getcwd()):
    components = 'Display.Driver NVI2 EULA.txt ListDevices.txt GFExperience/*.txt GFExperience/locales GFExperience/EULA.html GFExperience/PrivacyPolicy setup.cfg setup.exe'
    try:
        archiver = tuple(Path('C:\\').rglob('*7z.exe'))[0]
    except IndexError:
        print("Error: Couldn't find (7z.exe)!")
        archiver = None    
    if archiver != None:
        command = f'{archiver} x -bso0 -bsp1 -bse1 -aoa "{driver_file}" {components} -o"{dir}"'
        if run(command).returncode == 0:
            print(f'Unpacked to {Path(path.abspath(dir))}')

# Command Line Interface
parser = ArgumentParser(description = 'A tool that allows you to download NVIDIA Game Ready and Studio drivers via the command-line. Made with Python!')
arguments = parser.add_argument_group('Arguments').add_mutually_exclusive_group()
options = parser.add_argument_group('Options')
arguments.add_argument('-list', '-ls',
                        action = 'store_true', 
                        help = 'Show all available driver versions.')
arguments.add_argument('-download', '-dl',
                        nargs = 1,
                        help = 'Download the latest driver or a specified driver version.',
                        metavar='[Driver Version]')
arguments.add_argument('-unpack',
                        nargs = 1,
                        help = 'Unpack only the display driver from a driver package.',
                        metavar='[Driver File]')                        
options.add_argument('-studio', 
                    action = 'store_true', 
                    help = 'Set the driver type to Studio.')
options.add_argument('-dir', 
                    nargs = '?',
                    default = getcwd(), 
                    action='store', 
                    help = 'Specify the output directory.', 
                    metavar = 'Directory')
args = parser.parse_args()

if args.studio is True:
    driver_type = 'Studio'   
elif args.studio is False:
    driver_type = 'Game Ready' 
if args.list is True: 
    print(f'Looking for {driver_type} Drivers...')
    print('\n'.join(get_driver_versions(studio_drivers = args.studio)))
elif args.download is not None:
    print(f'Downloading {driver_type} Driver...')
    if args.download[0].lower() == 'latest':
        driver_version = None
        print('Requesting the latest version...')
    else:
        driver_version = args.download[0]
        print(f'Version: {driver_version}')
    download(driver_version = driver_version , studio_drivers = args.studio, dir = args.dir)
elif args.unpack is not None:
    print(f'Unpacking ({args.unpack[0]})...')
    unpack(args.unpack[0], dir = args.dir)         
else:
    parser.parse_args('-h'.split())
