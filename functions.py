
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
def get_driver_versions(studio_drivers = False):
    gr_driver_versions = () 
    studio_driver_versions = ()
    link = get_gpu()
    with urlopen(link) as file:
        file = [line.decode('UTF-8').strip() for line in file]      
    for line in file:
        if fnmatch(line, '<td class="gridItem">*.*</td>'):
            driver_version = line.split('>')[1].split('<')[0]
            if driver_version != '':
                gr_driver_versions += driver_version,
    if studio_drivers:
        for driver_version in gr_driver_versions:
            try:
                if WMI().Win32_Battery() == []: driver_link = STUDIO_DESKTOP_LINK 
                else: driver_link = STUDIO_NOTEBOOK_LINK 
                if urlopen(f'{driver_link}'.format(driver_version = driver_version)).getcode() == 200: 
                    studio_driver_versions += driver_version,
            except HTTPError:
                pass    
        return studio_driver_versions                          
    else:
        return gr_driver_versions           

# Download an NVIDIA Driver Package.
def download(driver_version = None, studio_drivers = False, dir = getcwd()):
    if path.exists(dir) is False:
        makedirs(path.abspath(dir))

    if driver_version is None:
        driver_versions = get_driver_versions(studio_drivers = studio_drivers)
    else:
        driver_versions = driver_version,  

    match studio_drivers:
        case True:
            prefix = 'Studio'
            if WMI().Win32_Battery() == []: driver_link = STUDIO_DESKTOP_LINK 
            else: driver_link = STUDIO_NOTEBOOK_LINK     
        case False:
            prefix = 'Game Ready'
            if WMI().Win32_Battery() == []: driver_link = GR_DESKTOP_LINK 
            else: driver_link = GR_NOTEBOOK_LINK    

    print('Checking Download...')
    try:
        if urlopen(f'{driver_link}'.format(driver_version = driver_versions[0])).getcode() == 200:
            print('Version is valid, now downloading NVIDIA Driver...')
            run(f'curl.exe -# "{driver_link}" -o "{dir}/{prefix} - {driver_versions[0]}.exe"'.format(driver_version = driver_versions[0]))       
    except:
        print("Version isn't valid...")  

# Unpack only the Display Driver from an NVIDIA Driver Package.
def unpack(driver_file, dir = getcwd()):
    try:
        archiver = tuple(Path('C:\\').rglob('*7z.exe'))[0]
    except IndexError:
        print("Error: Couldn't find (7z.exe)!")
        archiver = None    
    if archiver != None:
        command = f'{archiver} x -bso0 -bsp1 -bse1 -aoa "{driver_file}" {COMPONENTS} -o"{dir}"'
        if run(command).returncode == 0:
            print(f'Unpacked to {Path(path.abspath(dir))}')

# Check if your NVIDIA driver is outdated or not.
def update(studio_drivers = False):
    installed_driver_version = run(REG_KEY, capture_output = True).stdout.decode('UTF-8').split(' ')[-1].split('\r')[0]
    if installed_driver_version == get_driver_versions(studio_drivers = studio_drivers)[0]:
        print('The latest driver has been installed.')
    else:
        print('Your current driver is outdated! Please update!')     

# Get PSID and PFID of the installed NVIDIA GPU.
def get_gpu():
    index = ()
    for GPU in WMI().Win32_VideoController():
        gpu = GPU.wmi_property('Caption').value
        if 'nvidia' in gpu.lower():
            gpu = gpu.split("NVIDIA")[1].strip()
            break
    with urlopen('https://www.nvidia.com/Download/API/lookupValueSearch.aspx?TypeID=3') as file:
        lines = [line.decode('UTF-8').strip() for line in file.read().splitlines()]
    for x,y in enumerate(lines):
        if fnmatch(y, f'<Name>{gpu}</Name>'):
            index = lines[x-1].split('LookupValue ParentID="')[1].split('">')[0], lines[x+1].split('<')[1].split('>')[1]
    psid, pfid = index   
    return LINK.format(psid=psid, pfid=pfid, osid=57, lid=1, dtcid=1, dtid=1)      