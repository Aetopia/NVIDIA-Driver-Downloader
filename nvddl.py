# NVIDIA Driver Downloader made by Aetopia.
# GitHub Repository: https://github.com/Aetopia/NVIDIA-Driver-Downloader
# Discord: https://dsc.gg/CTT
# Under the MIT License: https://github.com/Aetopia/NVIDIA-Driver-Downloader/blob/main/LICENSE.md

from argparse import ArgumentParser
from os import getcwd
from functions import *

def main():
    parser = ArgumentParser(description = 'A tool that allows you to download NVIDIA Game Ready and Studio drivers via the command-line. Made with Python!')
    arguments = parser.add_argument_group('Arguments').add_mutually_exclusive_group()
    options = parser.add_argument_group('Options')
    arguments.add_argument('--list', '-ls',
                            action = 'store_true', 
                            help = 'Show all available driver versions.')
    arguments.add_argument('--download', '-dl',
                            nargs = 1,
                            help = 'Download the latest driver or a specified driver version.',
                            metavar='[Driver Version]')
    arguments.add_argument('--unpack',
                            nargs = 1,
                            help = 'Unpack only the display driver from a driver package.',
                            metavar='[Driver File]')   
    arguments.add_argument('--update',
                        action = 'store_true',
                        help = 'Check if the installed NVIDIA driver is outdated or not.')                                             
    options.add_argument('--studio', '-s',
                        action = 'store_true', 
                        help = 'Set the driver type to Studio.')
    options.add_argument('--dir', '-d',
                        nargs = '?',
                        default = getcwd(), 
                        action='store', 
                        help = 'Specify the output directory.', 
                        metavar = 'Directory')                    
    args = parser.parse_args()

    if args.studio is True: driver_type = 'Studio'   
    elif args.studio is False: driver_type = 'Game Ready' 
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
    elif args.update is True: update(studio_drivers = args.studio)          
    else: parser.parse_args('-h'.split())

if __name__ == '__main__':
    main()       