# NVIDIA Driver Downloader made by Aetopia.
# GitHub Repository: https://github.com/Aetopia/NVIDIA-Driver-Downloader
# Discord: https://dsc.gg/CTT
# Under the MIT License: https://github.com/Aetopia/NVIDIA-Driver-Downloader/blob/main/LICENSE.md

from os import getcwd
from urllib.request import urlopen, HTTPError
from argparse import ArgumentParser
from codecs import decode
from fnmatch import fnmatch
from subprocess import run
from sys import argv

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

parser = ArgumentParser(description = 'A tool that allows you to download NVIDIA Game Ready and Studio drivers via the command line. Made with Python!')
arguments = parser.add_argument_group('Arguments').add_mutually_exclusive_group(required = True)
options = parser.add_argument_group('Options')
arguments.add_argument('-list', '-ls',
                        action = 'store_true', 
                        help = 'Show all available driver versions.')
arguments.add_argument('-download', '-dl',
                        nargs = '?', 
                        action = 'store', 
                        default = '', 
                        type = str, 
                        help = 'Download the latest or specified driver version.', metavar='<Driver Version>')
options.add_argument('-type', 
                    nargs = 1, 
                    action = 'store', 
                    help = 'Specify the driver type.', 
                    metavar = '<GR/Studio>')
options.add_argument('-dir', 
                    nargs = 1, 
                    action='store', 
                    help = 'Specify the directory where the driver should be downloaded.', 
                    metavar = '<Directory>')
args = parser.parse_args()

if len(argv) != 1:
    try:
        if args.type[0].lower() == 'gr' or args.type[0].lower() == 'game ready':
                title = 'Looking for Game Ready Drivers...'
                studio_drivers = False
                type = 'Downloading Game Ready Driver...'
        elif args.type[0].lower() == 'studio': 
            title = 'Looking for Studio Drivers...' 
            studio_drivers = True  
            type = 'Downloading Studio Driver...'
    except:
        title = 'Looking for Game Ready Drivers...'
        studio_drivers = False 
        type = 'Downloading Game Ready Driver...'
    try:
        dir = args.dir[0]
    except:
        dir = getcwd()    
    if args.list is True: 
        print(title)
        print('\n'.join(get_driver_versions(studio_drivers = studio_drivers)))
    elif args.download is None:
        print(type)
        print('Requesting the latest version...')
        download(studio_drivers = studio_drivers, dir = dir)
    elif args.download is not None:
        print(type)
        print(f'Version: {args.download}')
        download(driver_version=args.download, studio_drivers = studio_drivers, dir = dir)  
else:
    parser.parse_args('-h'.split())
