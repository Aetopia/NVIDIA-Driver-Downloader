# NVIDIA Driver Downloader made by Aetopia.
# GitHub Repository: https://github.com/Aetopia/NVIDIA-Driver-Downloader
# Discord: https://dsc.gg/CTT
# Under the MIT License: https://github.com/Aetopia/NVIDIA-Driver-Downloader/blob/main/LICENSE.md

from traceback import format_exc
from plugins.textformat import fg, eol
from os import _exit
from tempfile import gettempdir
from logging import basicConfig, info, error, warning
from sys import argv, exit
from core.cli import cli

basicConfig(filename=f'{gettempdir()}/nvddl.log', filemode='w+',
            format='%(levelname)s: %(message)s', level='INFO')


if __name__ == '__main__':
    try:
        cli(argv[1:])
        info('Finished!')
        exit(0)
    except KeyboardInterrupt:
        print(f'\n{fg.lred}Warning: Operation Cancelled.{eol}')
        warning('Operation Cancelled.')
        _exit(1)

    except Exception as e:
        print(
            f'\n{fg.lred}Error: Found an uncatchable exception!\n> {e}\n')
        print(f'Check out the log and traceback files for more details.\nLog: "%TEMP%\\nvddl.log"\nTraceback: "%TEMP%\\nvddl_traceback.txt"{eol}')
        error('Found an uncatchable exception!')
        error(f'Exception: {e}')
        with open(f'{gettempdir()}/nvddl_traceback.txt', 'w') as f:
            f.write(format_exc())
        info('Exiting...')
        _exit(1)
