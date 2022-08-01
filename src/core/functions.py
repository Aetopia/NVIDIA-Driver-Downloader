# Modules
import logging
import os
import subprocess as sp
from fnmatch import fnmatch
from pathlib import Path
from shutil import rmtree
from urllib.error import HTTPError
from urllib.request import urlopen

import data.constants as csts
import plugins.utils as utils
from plugins.files import archiver
from plugins.textformat import eol, fg

logging.basicConfig(filename=f'{os.getenv("TEMP")}/nvddl.log', filemode='w+',
                    format='%(levelname)s: %(message)s', level='INFO')

# Flags -> Enables or replaces certain functions.


def flags(flags: list = []) -> None:
    if flags != []:
        print(f'{fg.lred}Warning: Using Flags!{eol}')
        logging.warning(f'Using Flags!')
        flags_verbose = ()
        for flag in flags:
            match flag.lower():
                case _:
                    logging.error(f'Invalid Flag > {flag}')
                    raise Exception(f'Invalid Flag > {flag}')

        for text in flags_verbose:
            print(text)
        print()

# Functions

# Get NVIDIA Driver Versions.


def get_driver_versions(studio_drivers=False, type='dch') -> tuple:
    if studio_drivers:
        logging.info('Selected Driver Type: Studio')
        whql = 4
    else:
        logging.info('Selected Driver Type: Game Ready')
        whql = 1

    if type.lower() == 'dch':
        logging.info('Selected Driver Type: DCH')
        dtcid = 1
    elif type.lower() == 'std':
        logging.info('Selected Driver Type: Standard')
        dtcid = 0

    try:
        gpu, psid, pfid = utils.get_gpu()
    except TypeError:
        logging.error('Couldn\'t get GPU!')
        raise Exception('Couldn\'t get GPU!')

    link = csts.API_LINK.format(psid=psid, pfid=pfid, whql=whql, dtcid=dtcid)
    logging.info(f'Detected: {gpu}')
    logging.info(F'API Link Generated: {link}')
    driver_versions = ()

    with urlopen(link) as file:
        file = [line.decode('UTF-8').strip() for line in file]

    for line in file:
        if fnmatch(line, '<td class="gridItem">*.*</td>'):
            driver_version = line.split('>')[1].split('<')[0]
            if driver_version != '':
                try:
                    float(driver_version)
                except ValueError:
                    driver_version = driver_version.split(
                        '(')[1].strip(')').strip()
                driver_versions += driver_version,

    if len(driver_versions) == 0:
        logging.error(f'Couldn\'t find any valid driver versions.')
        raise Exception(f'Couldn\'t find any valid driver versions.')
    return driver_versions

# Download an NVIDIA Driver Package.


def download(driver_version=None, studio_drivers=False,
             type='dch', output=os.getenv("TEMP"),
             full=False, components: list = [],
             setup=False, nvcpl=False) -> None:

    if type == 'dch':
        print(f'{fg.lyellow}Type: DCH{eol}')
    elif type == 'std':
        print(f'{fg.lyellow}Type: Standard{eol}')

    if full:
        print(f'{fg.lyellow}Package: Full{eol}')
    elif full is False:
        print(f'{fg.lyellow}Package: Custom{eol}')

    if os.path.exists(output) is False:
        os.makedirs(os.path.abspath(output))

    if driver_version is None:
        driver_version = get_driver_versions(
            studio_drivers=studio_drivers, type=type)[0]

    match studio_drivers:
        case True:
            prefix = 'Studio'
        case False:
            prefix = 'Game Ready'

    logging.info(
        f'Links Category: {prefix} {utils.system_type().capitalize()}')

    driver_links = utils.dl_links(driver_version, studio_drivers, type)
    filepath = f'{output}/{type.upper()} {prefix} - {driver_version}'

    print(f'{fg.lbeige}Checking Links...{eol}')
    for index, driver_link in enumerate(driver_links):
        try:
            if urlopen(f'{driver_link}'.format(driver_version=driver_version)).getcode() == 200:

                logging.info(f'Queried version is valid: {driver_version}')
                logging.info(f'Valid Link: {driver_link}'.format(
                    driver_version=driver_version))
                print(
                    f'{fg.lbeige}Queried version is valid, now downloading NVIDIA driver package...{eol}')

                curl_cmd = f'curl.exe -#L "{driver_link}" -o "{filepath}.exe"'.format(
                    driver_version=driver_version)
                logging.info(f'Curl Command: {curl_cmd}')
                if sp.run(curl_cmd).returncode == 0:

                    if full is False:
                        print(
                            f'{fg.lbeige}Trying to extract the downloaded driver package...{eol}')
                        extract(f"{filepath}.exe", components=components,
                                output=output, setup=setup, nvcpl=nvcpl)

                    elif full is True:
                        logging.info(f'Downloaded to "{filepath}.exe"')
                        if setup is False:
                            file = f'"C:\Windows\explorer.exe" /select,"{Path(file)}"'
                        print(
                            f'{fg.lgreen}Downloaded to "{Path(filepath)}.exe"{eol}')
                        sp.Popen(f"{filepath}.exe", shell=True, stdout=sp.DEVNULL, stderr=sp.STDOUT,
                                 cwd=filepath, creationflags=sp.DETACHED_PROCESS)
                    break

        except HTTPError:
            if index == len(driver_links)-1:
                logging.error('Queried version isn\'t valid!')
                raise Exception('Queried version isn\'t valid!')
            else:
                logging.info(f'Invalid Link: {driver_link}')

# Extract a driver package with the specified components.


def extract(driver_file, output=os.getenv("TEMP"), components: list = [], full=False, setup=False, nvcpl=False):
    if os.path.isfile(driver_file) is False:
        logging.error('Specified input is not a file.')
        raise Exception('Specified input is not a file.')

    # Initialize
    if full is False:
        for index, component in enumerate(components):
            match component.lower():
                case 'audio': components[index] = 'HDAudio'
                case 'physx': components[index] = 'PhysX'
                case _:
                    logging.error(
                        f'Invalid component(s) specified. | {component}')
                    raise Exception(
                        f'Invalid component(s) specified. | {component}')
        components += csts.BASE_COMPONENTS
        logging.info(f'Selected Components: {components}')
    else:
        components = []

    output = f'{output}/{os.path.split(os.path.splitext(driver_file)[0])[1]}'
    file = f'{output}/setup.exe'
    if os.path.exists(output):
        rmtree(output)

    # Extract
    archiver_cmd = f'{archiver()} x -bso0 -bsp1 -bse1 -aoa "{driver_file}" {" ".join(components).strip()} -o"{output}"'
    logging.info(f'Archiver Command: {archiver_cmd}')
    if sp.run(archiver_cmd).returncode == 0:

        if full is False:
            with open(f'{output}/setup.cfg', 'r+', encoding='UTF-8') as cfg:
                content = cfg.read().splitlines()
                cfg.seek(0)
                for line in cfg.read().splitlines():
                    if line.strip() in csts.SETUP:
                        content.pop(content.index(line))
            with open(f'{output}/setup.cfg', 'w', encoding='UTF-8') as cfg:
                cfg.write('\n'.join(content))

            with open(f'{output}/NVI2/presentations.cfg', 'r+', encoding='UTF-8') as cfg:
                cfg = cfg.read().splitlines()
                content = cfg
                presentations = csts.PRESENTATIONS
                for index, line in enumerate(cfg):
                    if fnmatch(line, f'{presentations[0]}*'):
                        content[index] = f'{presentations[0]} value=""/>'
                    elif fnmatch(line, f'{presentations[1]}*'):
                        content[index] = f'{presentations[1]} value=""/>'
            with open(f'{output}/NVI2/presentations.cfg', 'w', encoding='UTF-8') as cfg:
                cfg.write('\n'.join(content))

        print(f'{fg.lgreen}Extracted to "{Path(os.path.abspath(output))}"{eol}')
        logging.info(f'Extracted to "{Path(os.path.abspath(output))}"')

        if setup is False:
            file = f'"C:\Windows\explorer.exe" /select,"{Path(str(file))}"'
        sp.Popen(file, shell=True, stdout=sp.DEVNULL, stderr=sp.STDOUT,
                 cwd=output, creationflags=sp.DETACHED_PROCESS)

        if nvcpl is True:
            utils.install_nvcpl(output)

    else:
        logging.error(
            'Something went wrong while extracting the specified driver package.')
        raise Exception(
            'Something went wrong while extracting the specified driver package.')
# Check if your NVIDIA driver is outdated or not.


def update(studio_drivers=False, full=False, components: list = [], setup=False) -> None:

    if studio_drivers:
        print(f'{fg.lyellow}Type: Studio{eol}')
    else:
        print(f'{fg.lyellow}Type: Game Ready{eol}')
    latest_driver_version = float(
        get_driver_versions(studio_drivers=studio_drivers)[0])
    installed_driver_version = utils.get_installed_driver_version()

    if installed_driver_version == latest_driver_version:
        print(f'{fg.lgreen}The latest driver has been installed.{eol}')
        logging.info('The latest driver has been installed.')
        return

    elif installed_driver_version > latest_driver_version:
        texts = (
            f'{fg.lblue}Do you want to downgrade your driver?',
            f'{fg.lblue}Downgrade?',
            f"{fg.lred}The currently installed driver will not be downgraded.")

    elif installed_driver_version < latest_driver_version:
        texts = (
            f'{fg.lblue}Your current driver is outdated! Please update!',
            f'{fg.lblue}Update?',
            f"{fg.lred}The latest driver won't be downloaded.")
    print(texts[0])

    while True:
        option = input(f'{texts[1]} (Y/N) > {eol}')
        if option.lower().strip() in ('y', 'yes', ''):
            download(full=full, studio_drivers=studio_drivers,
                     components=components, setup=setup)
        elif option.lower().strip() in ('n', 'no'):
            print(texts[2]+eol)

        logging.info(f'Update/Downgrade Selected.')
        return
