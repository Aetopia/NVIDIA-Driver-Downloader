# Modules
from constants import * # constants.py
from os import getcwd, makedirs, path
from tempfile import gettempdir
from subprocess import Popen, DEVNULL, STDOUT
from urllib.request import urlopen 
from urllib.error import HTTPError
from pathlib import Path
from fnmatch import fnmatch
from subprocess import run
from sys import exit
from utils import *

# Functions

# Get NVIDIA Driver Versions.
def get_driver_versions(studio_drivers = False, type = 'dch') -> tuple:
    if studio_drivers: whql = 4
    else: whql = 1
    if type.lower() == 'dch': dtcid = 1
    elif type.lower() == 'std': dtcid = 0
    psid, pfid = get_gpu()
    link = API_LINK.format(psid = psid, pfid = pfid, whql = whql, dtcid = dtcid)
    driver_versions = ()

    with urlopen(link) as file:
        file = [line.decode('UTF-8').strip() for line in file]      
    for line in file:
        if fnmatch(line, '<td class="gridItem">*.*</td>'):
            driver_version = line.split('>')[1].split('<')[0]
            if driver_version != '':
                driver_versions += driver_version,  
    if len(driver_versions) == 0:
        print("Error: Couldn't find any valid driver versions.")
        exit()                  
    return driver_versions             

# Download an NVIDIA Driver Package.
def download(driver_version = None, studio_drivers = False, type = 'dch', dir = gettempdir(), minimal = False, components = ()):
    if type == 'dch': type = 'DCH';print('Type: DCH')
    elif type == 'std': type = 'STD';print('Type: Standard')

    if path.exists(dir) is False:
        makedirs(path.abspath(dir))

    if driver_version is None:
        driver_versions = get_driver_versions(studio_drivers = studio_drivers, type = type)
    else:
        driver_versions = driver_version,

    match studio_drivers:
        case True:
            prefix = 'Studio'
            match system_type(): 
                case 'laptop': driver_links = STUDIO_DESKTOP_LINKS[type]
                case 'desktop': driver_links = STUDIO_NOTEBOOK_LINKS[type]     
        case False:
            prefix = 'Game Ready'
            match system_type():
                case 'laptop': driver_links = GR_DESKTOP_LINKS[type] 
                case 'desktop': driver_links = GR_NOTEBOOK_LINKS[type]    

    print('Checking Download...')
    for index, driver_link in enumerate(driver_links):
        try:
            if urlopen(f'{driver_link}'.format(driver_version = driver_versions[0])).getcode() == 200:
                print('Version is valid, now downloading NVIDIA Driver Package...')
                if run(f'curl.exe -# "{driver_link}" -o "{dir}/{type} {prefix} - {driver_versions[0]}.exe"'.format(driver_version = driver_versions[0])).returncode != 0:
                    raise KeyboardInterrupt
                if minimal: 
                    print('Trying to unpack the downloaded Driver Package...')
                    filepath = f'{dir}/{type} {prefix} - {driver_versions[0]}'
                    unpack(f"{filepath}.exe", dir, components = components)
                    file = f'{filepath}/setup.exe'
                else: file = f'{filepath}.exe'
                Popen(file, shell=True, stdout = DEVNULL, stderr = STDOUT)    
                break           
        except HTTPError:
            if index == len(driver_links)-1:
                print("Error: Version isn't valid!")

# Unpack only the Display Driver from an NVIDIA Driver Package.
def unpack(driver_file, dir = getcwd(), components = []):
    for index, component in enumerate(components):
        match component.lower():
            case 'audio': components[index] = 'HDAudio'
            case _: components.pop(index)
    components += BASE_COMPONENTS

    dir = f'{dir}/{path.split(path.splitext(driver_file)[0])[1]}'

    try: archiver = tuple(Path('C:\\').rglob('*7z.exe'))[0]
    except IndexError:
        print("Error: Couldn't find (7z.exe)!")
        exit() 

    if run(f'{archiver} x -bso0 -bsp1 -bse1 -aoa "{driver_file}" {""" """.join(components).strip()} -o"{dir}"').returncode == 0:
        with open(f'{dir}/setup.cfg', 'r+', encoding='UTF') as file:
            content = file.read().splitlines(); file.seek(0)
            for line in file.read().splitlines():
                if line.strip() in SETUP: content.pop(content.index(line))
        with open(f'{dir}/setup.cfg', 'w', encoding = 'UTF-8') as file: file.write('\n'.join(content))                        
        print(f'Unpacked to "{Path(path.abspath(dir))}"')

# Check if your NVIDIA driver is outdated or not.
def update(studio_drivers = False) -> None:
    if studio_drivers: print('Type: Studio')
    else: print('Type: Game Ready')
    installed_driver_version = run(REG_KEY, capture_output = True).stdout.decode('UTF-8').split(' ')[-1].split('\r')[0]
    if installed_driver_version == get_driver_versions(studio_drivers = studio_drivers)[0]:
        print('The latest driver has been installed.')
    else:
        print('Your current driver is outdated! Please update!') 
        while True:
            option = input('Update? (Y/N): ')
            if option.lower().strip() in ('y','yes', ''):
                download(minimal = True); break
            elif option.lower().strip() in ('n', 'no'): print("The latest driver won't be downloaded."); break    
