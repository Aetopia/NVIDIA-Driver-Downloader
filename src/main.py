# NVIDIA Driver Downloader made by Aetopia.
# GitHub Repository: https://github.com/Aetopia/NVIDIA-Driver-Downloader
# Discord: https://dsc.gg/CTT
# Under the MIT License: https://github.com/Aetopia/NVIDIA-Driver-Downloader/blob/main/LICENSE.md

import logging
from os import _exit
from sys import argv, exit
from tempfile import gettempdir
from traceback import format_exc

from core.cli import cli
from plugins.textformat import eol, fg

logging.basicConfig(filename=f'{gettempdir()}/nvddl.log', filemode='w+',
            format='%(levelname)s: %(message)s', level='INFO')

def main():
    try:
        cli(argv[1:])
        logging.info('Finished!')
        exit(0)
    except KeyboardInterrupt:
        print(f'\n{fg.lred}Warning: Operation Cancelled.{eol}')
        logging.warning('Operation Cancelled.')
        _exit(1)

    except Exception as e:
        print(f'\n{fg.lred}An error has occured.\n> {e}\n{eol}')
        logging.error(f'Exception: {e}')
        with open(f'{gettempdir()}/nvddl_traceback.txt', 'w') as f:
            f.write(format_exc())
        logging.info('Exiting...')
        exit(1)

if __name__ == '__main__':
    main()
