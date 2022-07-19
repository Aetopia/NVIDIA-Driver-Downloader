from argparse import ArgumentParser, SUPPRESS, RawDescriptionHelpFormatter
from core.strings import HELP_DRIVER_OPTIONS, HELP_OPTIONS, HELP_ARGUMENTS, PROGRAM_DESCRIPTION
from core.functions import get_driver_versions, download, flags, extract, update
from plugins.textformat import fg, eol
from os import getcwd, path
import sys
from tempfile import gettempdir
from logging import basicConfig, info, error
from plugins.files import pciids, gpus 

basicConfig(filename=f'{gettempdir()}/nvddl.log', filemode='w+',
            format='%(levelname)s: %(message)s', level='INFO')

def cli(argv):
    parser = ArgumentParser(description=PROGRAM_DESCRIPTION,
                            formatter_class=RawDescriptionHelpFormatter,
                            add_help=False, usage=SUPPRESS)

    parser.add_argument('-h', '--help', action='store_true', help=SUPPRESS)

    arguments = parser.add_argument_group(title=' Arguments',
                                          description=HELP_ARGUMENTS)\
        .add_mutually_exclusive_group()

    driver_options = parser.add_argument_group(title=' Driver Options',
                                               description=HELP_DRIVER_OPTIONS)

    options = parser.add_argument_group(title=' Options',
                                        description=HELP_OPTIONS)

    arguments.add_argument('--list', '-ls',
                           action='store_true',
                           help=SUPPRESS)

    arguments.add_argument('--download', '-dl',
                           nargs='?',
                           help=SUPPRESS,
                           metavar='Driver Version')

    arguments.add_argument('--extract', '-e',
                           nargs=1,
                           help=SUPPRESS,
                           metavar='<Driver File>')

    arguments.add_argument('--update', '-u',
                           action='store_true',
                           help=SUPPRESS)

    driver_options.add_argument('--studio', '-stu',
                                action='store_true',
                                help=SUPPRESS)

    driver_options.add_argument('--standard', '-std',
                                action='store_true',
                                help=SUPPRESS)

    driver_options.add_argument('--full', '-f',
                                action='store_true',
                                help=SUPPRESS)

    driver_options.add_argument('--setup', '-s',
                                action='store_true',
                                help=SUPPRESS)

    options.add_argument('--components', '-c',
                         action='store',
                         metavar=('Component', 'Components'),
                         default=[],
                         nargs='+',
                         help=SUPPRESS)

    options.add_argument('--output', '-o',
                         nargs='?',
                         default=gettempdir(),
                         action='store',
                         help=SUPPRESS,
                         metavar='Directory')

    options.add_argument('--flags',
                         action='store',
                         metavar=('Flag', 'Flags'),
                         nargs='+',
                         default=[],
                         help=SUPPRESS)

    parser.add_argument('--no-stdout',
                        action='store_true',
                        help=SUPPRESS)
    parse(parser.parse_known_args(argv), argv, parser)

def parse(args, argv, parser):
    args = args[0]
    info(f'Namespace: {args}')
    info(f'Arguments: {argv}')

    if args.help:
        argv = []

    flags(args.flags)
    if args.no_stdout:
        sys.stdout = None

    if len(argv) != 0:
        if not ('-dl' in argv or '--download' in argv
                or '-u' in argv or '--update' in argv
                or '--extract' in argv or '-e' in argv
                or '-ls' in argv or '--list' in argv):
            parser.print_usage()
            error('No arguments detected.')
            raise Exception('No arguments detected.')

        gpus().fetch();pciids().fetch()
        if args.output is None:
            args.output = getcwd()
        match args.studio:
            case True: driver_type = 'Studio'
            case False: driver_type = 'Game Ready'

        match args.standard:
            case True:
                type = 'std'
                driver_type = f'Standard {driver_type}'
            case False:
                type = 'dch'
                driver_type = f'DCH {driver_type}'

        if args.list is True:
            info('Getting Driver Versions...')
            print(f'{fg.lyellow}{driver_type} Drivers:{eol}')
            driver_versions = get_driver_versions(
                studio_drivers=args.studio, type=type)

            for index, driver_version in enumerate(driver_versions):
                if index == 0:
                    print(f' {fg.lgreen}~ {driver_version}{eol}')
                elif index+1 == len(driver_versions):
                    print(f' {fg.lviolet}# {driver_version}{eol}')
                else:
                    print(f' {fg.lbeige}> {driver_version}{eol}')

        elif args.extract is not None:
            info('Extracting Driver...')
            print(
                f'{fg.lyellow}Extracting ({path.split(args.extract[0])[1].strip()})...{eol}')
            extract(args.extract[0], output=args.output,
                    components=args.components,
                    full=args.full, setup=args.setup)

        elif args.update is True:
            info('Updating Driver...')
            update(studio_drivers=args.studio,
                   components=args.components, setup=args.setup)

        elif args.download is not None:
            info('Downloading Driver...')
            print(f'{fg.lyellow}Downloading {driver_type} Driver...{eol}')
            driver_version = args.download
            print(f'{fg.lyellow}Version: {driver_version}{eol}')

            download(driver_version=driver_version, studio_drivers=args.studio,
                     type=type, output=args.output,
                     full=args.full, components=args.components, setup=args.setup)

        elif args.download is None:
            info('Downloading Driver...')
            print(
                f'{fg.lyellow}Downloading the Latest {driver_type} Driver...{eol}')

            download(studio_drivers=args.studio, type=type,
                     output=args.output, full=args.full,
                     components=args.components, setup=args.setup)
    else:
        parser.print_help()
