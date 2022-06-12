from tempfile import gettempdir
from wmi import WMI 
from xml.etree import ElementTree
from winreg import HKEY_LOCAL_MACHINE, OpenKey, EnumValue
from urllib.request import urlopen
from subprocess import run
from pathlib import Path
from sys import exit
from textformat import *
from traceback import format_exc
from os import path, startfile

# Get PSID and PFID of the installed NVIDIA GPU.
def get_psid_pfid() -> tuple:
    gpu_list = gpus()
    IS_NOT_NVIDIA = False

    for detected_gpus in WMI().Win32_VideoController():
        detected_gpu = detected_gpus.Caption
        if 'nvidia' in detected_gpu.lower():
            for gpu in gpu_list.keys():
                if gpu in detected_gpu:
                    return gpu_list[gpu]['PSID'], gpu_list[gpu]['PFID']
        else: IS_NOT_NVIDIA = True

    if IS_NOT_NVIDIA: 
        print(f'{fg.lred}Warning: No NVIDIA GPU detected, using fallback mode.\n{eol}')
        return gpu_list['GeForce GTX 1050']['PSID'], gpu_list['GeForce GTX 1050']['PFID']
    
# Parse the GPU List XML file into a dictionary.
def gpus() -> dict:
    response = {}
    xml = ElementTree.parse(urlopen('https://www.nvidia.com/Download/API/lookupValueSearch.aspx?TypeID=3')).getroot()
    for index, tag in enumerate(xml.findall('LookupValues/LookupValue')):
        response[tag[0].text] =  {'PSID': str(index), 'PFID':tag[1].text}
    return response

# Detect if the device being used is a laptop or desktop. (Thanks Felipe#5555! :3)
def system_type() -> str:
    type = [system.wmi_property('ChassisTypes').value[0] for system in WMI().Win32_SystemEnclosure()][0]
    if type in (8, 9, 10, 11, 12, 14, 18, 21):
        return 'laptop'
    elif type in (3, 4, 5, 6, 7, 15, 16):
        return 'desktop'
    else:
        print(f"{fg.lred}Error: Couldn't detect system type.{eol}")
        exit(1)                         

def get_drives():
    drives = ()
    for drive in WMI().Win32_LogicalDisk():
        drives += f'{drive.DeviceID}\\',
    return drives    

def get_installed_driver_version() -> float:
    try: query_key = OpenKey(HKEY_LOCAL_MACHINE, 
                             r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\{B2FE1952-0186-46C3-BAEC-A80AA35AC5B8}_Display.Driver")
    except FileNotFoundError: print(f'{fg.lred}Error: NVIDIA Display Driver is not installed.{eol}'); exit(1)    
    index = 0
    while True:
        try:
            key, value, _ = EnumValue(query_key, index)
            if key == 'DisplayVersion':
                try: return float(value)
                except ValueError: print(f'{fg.lred}Error: NVIDIA Display Driver is not installed.{eol}'); exit(1)
        except OSError: break     
        index += 1

def get_archiver():
    drives = get_drives()
    returncode = None
    try:
        for drive in drives:
            for archiver in Path(drive).rglob('*7z.exe'):

                try: returncode = run(archiver, capture_output = True).returncode
                except FileNotFoundError: returncode = None   
                except OSError: returncode = None    

                if returncode == 0: break
            if returncode == 0: break
        return archiver        
    except UnboundLocalError: print(f"{fg.lred}Error: Couldn't find a usable archiving program.{eol}"); exit(1)  

def traceback_log() -> None:
    lines = []
    for line in format_exc().splitlines():
        if '  File' in line[0:6]:
            line = line.split('",', 1); file = path.split(line[0].split("  File ")[1].lstrip('"'))[1]
            line[0] = f'  File "{file}",'; line = ''.join(line)
        lines += [line]
    with open(f'{gettempdir()}/nvddl_traceback.txt', 'w') as f: f.write('\n'.join(lines))
    startfile(f'{gettempdir()}/nvddl_traceback.txt', 'open')
