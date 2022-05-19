# NVIDIA Driver Downloader made by Aetopia.
# GitHub Repository: https://github.com/Aetopia/NVIDIA-Driver-Downloader
# Discord: https://dsc.gg/CTT
# Under the MIT License: https://github.com/Aetopia/NVIDIA-Driver-Downloader/blob/main/LICENSE.md

from argparse import ArgumentParser
from functions import *
from os import getcwd, path
from sys import argv, exit
from tempfile import gettempdir

def main():
    parser = ArgumentParser(description = 'A tool that allows you to download NVIDIA Game Ready and Studio drivers via the command-line. Made with Python!')
    arguments = parser.add_argument_group('Arguments').add_mutually_exclusive_group()
    options = parser.add_argument_group('Options')
    arguments.add_argument('--list', '-ls',
                            action = 'store_true', 
                            help = 'Show all available driver versions.')
    arguments.add_argument('--download', '-dl',
                            nargs = '?',
                            help = 'Download the latest driver or a specified driver version.',
                            metavar='Driver Version')
    arguments.add_argument('--extract', '-e',
                            nargs = 1,
                            help = 'Extract the specified driver package.',
                            metavar='<Driver File>')   
    arguments.add_argument('--update', '-up',
                        action = 'store_true',
                        help = 'Check if the installed NVIDIA driver is outdated or not.')                                             
    options.add_argument('--studio', '-s',
                        action = 'store_true', 
                        help = 'Set the driver type to Studio.')
    options.add_argument('--standard', '-std',
                         action = 'store_true',
                         help='Set the driver type to Standard.')
    options.add_argument('--output', '-o',
                        nargs = '?',
                        default = gettempdir(), 
                        action='store', 
                        help = 'Specify the output directory.', 
                        metavar = 'Directory') 
    options.add_argument('--minimal', '-m',
                        action = 'store_true',
                        help='Debloat a driver package as soon as its downloaded.')   
    options.add_argument('--components','-c',
                        action = 'store',
                        metavar = ('Component', 'Components'),
                        nargs = '+',
                        help = 'Select which components to include in the driver package.')                                                        
    args = parser.parse_args()

    if len(argv) != 1: 
        if ('-dl' or '--download' or '-up' or '--update' or '--extract' or '-e' or 'ls' or '--list') in argv:
            if args.output is None: args.output = getcwd()
            if args.components is None: args.components = []
            match args.studio: 
                case True: driver_type = 'Studio'   
                case False: driver_type = 'Game Ready' 
            match args.standard:
                case True: type = 'std'
                case False: type = 'dch'
        else: 
            parser.print_usage() 
            print('Error: Options must be used with arguments.')
            exit()  
            
        if args.list is True: 
            print(f'{driver_type} Drivers:')
            print('\n'.join(get_driver_versions(studio_drivers = args.studio, type = type)))

        elif args.extract is not None:
            print(f'extracting ({path.split(args.extract[0])[1]})...')
            extract(args.extract[0], output = args.output, components = args.components)   

        elif args.update is True: update(studio_drivers = args.studio)  

        elif args.download is not None:
            print(f'Downloading {driver_type} Driver...')
            driver_version = args.download
            print(f'Version: {driver_version}')
            download(driver_version = driver_version , studio_drivers = args.studio, type = type, output = args.output, minimal = args.minimal, components = args.components)
        elif args.download is None:
            print(f'Downloading the Latest {driver_type} Driver...')
            download(studio_drivers = args.studio, type = type, output = args.output, minimal = args.minimal, components = args.components)  
    else: parser.print_help()

if __name__ == '__main__':
    try: main()
    except KeyboardInterrupt:
        print('\nWarning: Operation cancelled.')
        exit()           