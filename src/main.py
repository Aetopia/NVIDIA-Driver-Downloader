# NVIDIA Driver Downloader made by Aetopia.
# GitHub Repository: https://github.com/Aetopia/NVIDIA-Driver-Downloader
# Discord: https://dsc.gg/CTT
# Under the MIT License: https://github.com/Aetopia/NVIDIA-Driver-Downloader/blob/main/LICENSE.md

from argparse import ArgumentParser, SUPPRESS, RawDescriptionHelpFormatter
from constants import HELP_DRIVER_OPTIONS, HELP_OPTIONS, HELP_ARGUMENTS, PROGRAM_DESCRIPTION
from functions import *
from colors import printc, getc
from os import getcwd, path
from sys import argv, exit
from tempfile import gettempdir
from traceback import print_exc

def main():
    parser = ArgumentParser(description = getc(PROGRAM_DESCRIPTION), 
    formatter_class = RawDescriptionHelpFormatter,
    add_help=False, usage=SUPPRESS)

    parser.add_argument('--help', action = 'help', help = SUPPRESS)

    arguments = parser.add_argument_group(title = ' Arguments', 
                                          description = HELP_ARGUMENTS)\
                                        .add_mutually_exclusive_group()

    driver_options = parser.add_argument_group(title = ' Driver Options',
                                               description = HELP_DRIVER_OPTIONS)

    options = parser.add_argument_group(title = ' Options',
                                        description = HELP_OPTIONS)

    arguments.add_argument('--list', '-ls',
                            action = 'store_true', 
                            help = SUPPRESS)

    arguments.add_argument('--download', '-dl',
                            nargs = '?',
                            help = SUPPRESS,
                            metavar='Driver Version')

    arguments.add_argument('--extract', '-e',
                            nargs = 1,
                            help = SUPPRESS,
                            metavar='<Driver File>') 

    arguments.add_argument('--update', '-u',
                        action = 'store_true',
                        help = SUPPRESS)  

    driver_options.add_argument('--studio', '-stu',
                        action = 'store_true', 
                        help = SUPPRESS)

    driver_options.add_argument('--standard', '-std',
                         action = 'store_true',
                         help = SUPPRESS)
                        
    driver_options.add_argument('--full', '-f',
                        action = 'store_true',
                        help = SUPPRESS) 
                          
    driver_options.add_argument('--setup', '-s',
                        action = 'store_true',
                        help = SUPPRESS)  
                         
    options.add_argument('--components','-c',
                        action = 'store',
                        metavar = ('Component', 'Components'),
                        default = [],
                        nargs = '+',
                        help = SUPPRESS) 

    options.add_argument('--output', '-o',
                        nargs = '?',
                        default = gettempdir(), 
                        action='store', 
                        help = SUPPRESS, 
                        metavar = 'Directory')   

    options.add_argument('--flags',
                         action = 'store',
                         metavar = ('Flag','Flags'),
                         nargs = '+',
                         default = [],
                         help = SUPPRESS)   

    args = parser.parse_args()
    flags(args.flags)
    if len(argv) != 1: 
        if not ('-dl' in argv or '--download' in argv \
           or '-u' in argv or '--update' in argv \
           or '--extract' in argv or '-e' in argv \
           or '-ls' in argv or '--list' in argv):
           parser.print_usage() 
           printc('@LREDError: Options must be used with arguments.')
           exit()   

        if args.output is None: args.output = getcwd()
        match args.studio: 
            case True: driver_type = 'Studio'   
            case False: driver_type = 'Game Ready' 

        match args.standard:
            case True: type = 'std'; driver_type = f'Standard {driver_type}'
            case False: type = 'dch'; driver_type = f'DCH {driver_type}'   

        if args.list is True: 
            printc(f'@LYELLOW{driver_type} Drivers:')
            driver_versions = get_driver_versions(studio_drivers = args.studio, type = type)

            for index, driver_version in enumerate(driver_versions):
                if index == 0: printc(f' @LGREEN~ {driver_version}') 
                elif index+1 == len(driver_versions): printc(f' @LVIOLET# {driver_version}')
                else: printc(f' @LBEIGE> {driver_version}')
                
        elif args.extract is not None:
            printc(f'@LYELLOWExtracting ({path.split(args.extract[0])[1].strip()})...')
            extract(args.extract[0], output = args.output, 
                    components = args.components, 
                    full = args.full, setup = args.setup)   

        elif args.update is True: update(studio_drivers = args.studio, components = args.components, setup = args.setup)  

        elif args.download is not None:
            printc(f'@LYELLOWDownloading {driver_type} Driver...')
            driver_version = args.download
            printc(f'@LYELLOWVersion: {driver_version}')

            download(driver_version = driver_version, studio_drivers = args.studio, 
                     type = type, output = args.output, 
                     full = args.full, components = args.components, setup = args.setup)
                     
        elif args.download is None:
            printc(f'@LYELLOWDownloading the Latest {driver_type} Driver...')
            
            download(studio_drivers = args.studio, type = type, 
                     output = args.output, full = args.full, 
                     components = args.components, setup = args.setup)  
    else: 
        parser.print_help()

if __name__ == '__main__':
    try: main()
    except KeyboardInterrupt: printc('@LREDWarning: Operation cancelled.');exit(1)
    except: printc('\n@LREDAn Error has occurred:');print_exc();exit()           