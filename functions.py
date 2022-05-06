# Modules
from constants import * # constants.py
from os import getcwd, makedirs, path
from urllib.request import urlopen 
from urllib.error import HTTPError
from pathlib import Path
from wmi import WMI
from fnmatch import fnmatch
from subprocess import run

# Functions

# Get NVIDIA Driver Versions.
def get_driver_versions(studio_drivers = False) -> tuple:
    if studio_drivers: whql = 4
    else: whql = 1
    psid, pfid = detect_gpu()
    link = LINK.format(psid = psid, pfid = pfid, whql = whql)
    driver_versions = ()

    with urlopen(link) as file:
        file = [line.decode('UTF-8').strip() for line in file]      
    for line in file:
        if fnmatch(line, '<td class="gridItem">*.*</td>'):
            driver_version = line.split('>')[1].split('<')[0]
            if driver_version != '':
                driver_versions += driver_version,           
    return driver_versions             

# Download an NVIDIA Driver Package.
def download(driver_version = None, studio_drivers = False, dir = getcwd()):
    if path.exists(dir) is False:
        makedirs(path.abspath(dir))

    if driver_version is None:
        driver_versions = get_driver_versions(studio_drivers = studio_drivers)
        if len(driver_versions) == 0:
            print("Error: Couldn't find any valid driver versions.")
            exit(1) 
    else:
        driver_versions = driver_version,  

    match studio_drivers:
        case True:
            prefix = 'Studio'
            if WMI().Win32_Battery() == []: driver_links = STUDIO_DESKTOP_LINK 
            else: driver_links = STUDIO_NOTEBOOK_LINK     
        case False:
            prefix = 'Game Ready'
            if WMI().Win32_Battery() == []: driver_links = GR_DESKTOP_LINK 
            else: driver_links = GR_NOTEBOOK_LINK    

    print('Checking Download...')
    for index, driver_link in enumerate(driver_links):
        try:
            if urlopen(f'{driver_link}'.format(driver_version = driver_versions[0])).getcode() == 200:
                print('Version is valid, now downloading NVIDIA Driver...')
                run(f'curl.exe -# "{driver_link}" -o "{dir}/{prefix} - {driver_versions[0]}.exe"'.format(driver_version = driver_versions[0])) 
                break           
        except HTTPError:
            if index == len(driver_links)-1:
                print("Error: Version isn't valid!")

# Unpack only the Display Driver from an NVIDIA Driver Package.
def unpack(driver_file, dir = getcwd()):
    dir = f'{dir}/{path.splitext(driver_file)[0]}'

    try: archiver = tuple(Path('C:\\').rglob('*7z.exe'))[0]
    except IndexError:
        print("Error: Couldn't find (7z.exe)!")
        exit(1) 

    if run(f'{archiver} x -bso0 -bsp1 -bse1 -aoa "{driver_file}" {COMPONENTS} -o"{dir}"').returncode == 0:
        print(f'Unpacked to "{Path(path.abspath(dir))}"')

# Check if your NVIDIA driver is outdated or not.
def update(studio_drivers = False) -> None:
    installed_driver_version = run(REG_KEY, capture_output = True).stdout.decode('UTF-8').split(' ')[-1].split('\r')[0]
    if installed_driver_version == get_driver_versions(studio_drivers = studio_drivers)[0]:
        print('The latest driver has been installed.')
    else:
        print('Your current driver is outdated! Please update!')     

# Get PSID and PFID of the installed NVIDIA GPU.
def detect_gpu() -> tuple:
    for GPU in WMI().Win32_VideoController():
        gpu = GPU.wmi_property('Caption').value
        if 'nvidia' in gpu.lower():
            if 'geforce' in gpu.lower():
                gpu = gpu.split("NVIDIA")[1].strip()
            break
        else:
            # Fallback Mode
            gpu = 'GeForce GTX 1050'    
    ids = gpus()[gpu] 
    return ids['PSID'], ids['PFID']

# Parse the GPU List XML file into a dictionary.
def gpus() -> dict:
    response = {}
    with urlopen('https://www.nvidia.com/Download/API/lookupValueSearch.aspx?TypeID=3') as file:
        lines = [line.decode('UTF-8').strip() for line in file.read().splitlines()]
    for x, y in enumerate(lines):
        if fnmatch(y, f'<Name>*</Name>'): 
            if y.split('<Name>')[1].split('</Name>')[0] not in response.keys():
                response[y.split('<Name>')[1].split('</Name>')[0]] = {'PSID':lines[x-1].split('LookupValue ParentID="')[1].split('">')[0], 'PFID':lines[x+1].split('<')[1].split('>')[1]}
    return response     