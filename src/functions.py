# Modules
from shutil import rmtree
from constants import QUADRO_LINKS, STUDIO_DESKTOP_LINKS, STUDIO_NOTEBOOK_LINKS, GR_DESKTOP_LINKS, GR_NOTEBOOK_LINKS, API_LINK, BASE_COMPONENTS, SETUP, PRESENTATIONS  # constants.py
from os import makedirs, path
from tempfile import gettempdir
from subprocess import Popen, DEVNULL, STDOUT, DETACHED_PROCESS
from urllib.request import urlopen
from urllib.error import HTTPError
from pathlib import Path
from fnmatch import fnmatch
from subprocess import run
from utils import get_archiver, get_installed_driver_version, system_type, get_psid_pfid
from ast import literal_eval
from textformat import fg, eol
from logging import basicConfig, info, error, warning
from sys import exit

basicConfig(filename=f'{gettempdir()}/nvddl.log', filemode='w+',
            format='%(levelname)s: %(message)s', level='INFO')

# Flags -> Enables or replaces certain functions.


def flags(flags: list = []) -> None:
    if flags != []:
        print(f'{fg.lred}Warning: Using Flags!{eol}')
        warning(f'Using Flags!')
        flags_verbose = ()
        for flag in flags:
            match flag.lower():
                case _:
                    print(f'{fg.lred}Error: Invalid Flag > {flag}{eol}')
                    error(f'Invalid Flag > {flag}')
                    exit(1)

        for text in flags_verbose:
            print(text)
        print()

# Functions

# Get NVIDIA Driver Versions.


def get_driver_versions(studio_drivers=False, type='dch') -> tuple:
    if studio_drivers:
        info('Selected Driver Type: Studio')
        whql = 4
    else:
        info('Selected Driver Type: Game Ready')
        whql = 1

    if type.lower() == 'dch':
        info('Selected Driver Type: DCH')
        dtcid = 1
    elif type.lower() == 'std':
        info('Selected Driver Type: Standard')
        dtcid = 0

    psid, pfid = get_psid_pfid()
    link = API_LINK.format(psid=psid, pfid=pfid, whql=whql, dtcid=dtcid)
    info(F'API Link Generated: {link}')
    driver_versions = ()

    with urlopen(link) as file:
        file = [line.decode('UTF-8').strip() for line in file]

    for line in file:
        if fnmatch(line, '<td class="gridItem">*.*</td>'):
            driver_version = line.split('>')[1].split('<')[0]
            if driver_version != '':
                driver_versions += driver_version,

    if len(driver_versions) == 0:
        print(f"{fg.lred}Error: Couldn't find any valid driver versions.{eol}")
        error(f'Couldn\'t find any valid driver versions.')
        exit(1)
    return driver_versions

# Download an NVIDIA Driver Package.


def download(driver_version=None, studio_drivers=False,
             type='dch', output=gettempdir(),
             full=False, components: list = [],
             setup=False) -> None:

    if type == 'dch':
        type = 'DCH'
        print(f'{fg.lyellow}Type: DCH{eol}')
    elif type == 'std':
        type = 'STD'
        print(f'{fg.lyellow}Type: Standard{eol}')
    if full:
        print(f'{fg.lyellow}Package: Full{eol}')
    elif full is False:
        print(f'{fg.lyellow}Package: Custom{eol}')

    if path.exists(output) is False:
        makedirs(path.abspath(output))

    if driver_version is None:
        driver_versions = get_driver_versions(
            studio_drivers=studio_drivers, type=type)
    else:
        driver_versions = driver_version,

    match studio_drivers:
        case True:
            prefix = 'Studio'
            match system_type():
                case 'notebook':
                    driver_links = STUDIO_NOTEBOOK_LINKS[type]
                    info('Links Category: Studio Notebook')

                case 'desktop':
                    driver_links = STUDIO_DESKTOP_LINKS[type]
                    info('Links Category: Studio Desktop')

        case False:
            prefix = 'Game Ready'
            match system_type():
                case 'notebook':
                    driver_links = GR_NOTEBOOK_LINKS[type]
                    info('Links Category: Game Ready Notebook')

                case 'desktop':
                    driver_links = GR_DESKTOP_LINKS[type]
                    info('Links Category: Game Ready Desktop')
    
    # Quadro Card Detection.
    try:
        float(driver_versions[0])
    except ValueError:
        driver_versions = driver_versions[0].split('(')[1].strip(')').strip(),
        driver_links = QUADRO_LINKS

    filepath = f'{output}/{type} {prefix} - {driver_versions[0]}'
    print(f'{fg.lbeige}Checking Links...{eol}')
    for index, driver_link in enumerate(driver_links):
        try:
            if urlopen(f'{driver_link}'.format(driver_version=driver_versions[0])).getcode() == 200:
                info(f'Queried version is valid: {driver_versions[0]}')
                info(f'Valid Link: {driver_link}'.format(
                    driver_version=driver_versions[0]))
                print(
                    f'{fg.lbeige}Queried version is valid, now downloading NVIDIA driver package...{eol}')
                curl_cmd = f'curl.exe -#L "{driver_link}" -o "{filepath}.exe"'.format(
                    driver_version=driver_versions[0])
                info(f'Curl Command: {curl_cmd}')
                if run(curl_cmd).returncode == 0:
                    if full is False:
                        print(
                            f'{fg.lbeige}Trying to extract the downloaded driver package...{eol}')
                        extract(f"{filepath}.exe", components=components,
                                output=output, setup=setup)

                    elif full is True:
                        info(f'Downloaded to "{filepath}.exe"')
                        if setup is False:
                            file = f'"C:\Windows\explorer.exe" /select,"{Path(file)}"'
                        print(
                            f'{fg.lgreen}Downloaded to "{Path(filepath)}.exe"{eol}')
                        Popen(f"{filepath}.exe", shell=True, stdout=DEVNULL, stderr=STDOUT,
                              cwd=filepath, creationflags=DETACHED_PROCESS)
                    break

        except HTTPError:
            if index == len(driver_links)-1:
                print(f"{fg.lred}Error: Queried version isn't valid!{eol}")
                error('Queried version isn\'t valid!')
                exit(1)
            else:
                info(f'Invalid Link: {driver_link}')

# Extract a driver package with the specified components.


def extract(driver_file, output=gettempdir(), components: list = [], full=False, setup=False):
    if path.isfile(driver_file) is False:
        print(f"{fg.lred}Error: Specified input is not a file.{eol}")
        error('Specified input is not a file.')
        exit(1)

    # Initialize
    if full is False:
        for index, component in enumerate(components):
            match component.lower():
                case 'audio': components[index] = 'HDAudio'
                case 'physx': components[index] = 'PhysX'
                case _:
                    print(f'{fg.lred}Error: Invalid component(s) specified.{eol}')
                    error(
                        f'Invalid component(s) specified. | {component}')
                    exit(1)
        components += BASE_COMPONENTS
        info(f'Selected Components: {components}')
    else:
        components = []

    output = f'{output}/{path.split(path.splitext(driver_file)[0])[1]}'
    file = f'{output}/setup.exe'
    if path.exists(output):
        rmtree(output)

    # Extract
    archiver = get_archiver()
    archiver_cmd = f'{archiver} x -bso0 -bsp1 -bse1 -aoa "{driver_file}" {" ".join(components).strip()} -o"{output}"'
    info(f'Archiver Command: {archiver_cmd}')
    if run(archiver_cmd).returncode == 0:

        if full is False:
            with open(f'{output}/setup.cfg', 'r+', encoding='UTF-8') as cfg:
                content = cfg.read().splitlines(); cfg.seek(0)
                for line in cfg.read().splitlines():
                    if line.strip() in SETUP:
                        content.pop(content.index(line))
            with open(f'{output}/setup.cfg', 'w', encoding='UTF-8') as cfg:
                cfg.write('\n'.join(content))

            with open(f'{output}/NVI2/presentations.cfg', 'r+', encoding='UTF-8') as cfg:
                cfg = cfg.read().splitlines()
                content = cfg
                for index, line in enumerate(cfg):
                    if fnmatch(line, f'{PRESENTATIONS[0]}*'):
                        content[index] = f'{PRESENTATIONS[0]} value=""/>'
                    elif fnmatch(line, f'{PRESENTATIONS[1]}*'):
                        content[index] = f'{PRESENTATIONS[1]} value=""/>'
            with open(f'{output}/NVI2/presentations.cfg', 'w', encoding='UTF-8') as cfg:
                cfg.write('\n'.join(content))

        print(f'{fg.lgreen}Extracted to "{Path(path.abspath(output))}"{eol}')
        info(f'Extracted to "{Path(path.abspath(output))}"')

        if setup is False:
            file = f'"C:\Windows\explorer.exe" /select,"{Path(str(file))}"'
        Popen(file, shell=True, stdout=DEVNULL, stderr=STDOUT,
              cwd=output, creationflags=DETACHED_PROCESS)

    else:
        print(
            f'{fg.lred}Error: Something went wrong while extracting the specified driver package.{eol}')
        error('Something went wrong while extracting the specified driver package.')
# Check if your NVIDIA driver is outdated or not.


def update(studio_drivers=False, full=False, components: list = [], setup=False) -> None:

    if studio_drivers:
        print(f'{fg.lyellow}Type: Studio{eol}')
    else:
        print(f'{fg.lyellow}Type: Game Ready{eol}')
    latest_driver_versions = literal_eval(
        get_driver_versions(studio_drivers=studio_drivers)[0])
    installed_driver_version = get_installed_driver_version()

    if installed_driver_version == latest_driver_versions:
        print(f'{fg.lgreen}The latest driver has been installed.{eol}')
        info('The latest driver has been installed.')
        exit(0)

    elif installed_driver_version > latest_driver_versions:
        texts = (
            f'{fg.lblue}Do you want to downgrade your driver?',
            f'{fg.lblue}Downgrade?',
            f"{fg.lred}The currently installed driver will not be downgraded.")

    else:
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
            info(f'Update/Downgrade Selected.')
            break
        elif option.lower().strip() in ('n', 'no'):
            print(texts[2]+eol)
            info('Update/Downgrade cancelled.')
            break
