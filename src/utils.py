from wmi import WMI
from winreg import HKEY_LOCAL_MACHINE, OpenKey, EnumValue
from subprocess import run
from pathlib import Path
from textformat import fg, eol
from logging import basicConfig, info, error
from helpers import *
from tempfile import gettempdir

basicConfig(filename=f'{gettempdir()}/nvddl.log', filemode='w+',
            format='%(levelname)s: %(message)s', level='INFO')

# Get PSID and PFID of the installed NVIDIA GPU.


def get_psid_pfid() -> tuple:
    gpu_list = gpus()
    detected_gpu = get_gpu()

    for gpu in gpu_list.keys():
        if gpu in detected_gpu:
            return gpu_list[gpu]['PSID'], gpu_list[gpu]['PFID']


def get_gpu(log=True):
    def message(): print(f'{fg.lred}Error: No NVIDIA GPU Detected.{eol}'); error(
        'No NVIDIA GPU Detected.'); exit(1)
    """
    Get the GPU name using a Hardware ID.
    """
    vendor_filter = '10DE'
    devices = ()

    for driver in WMI().Win32_PnPSignedDriver():
        try:
            hwid = driver.HardwareID.split(
                'PCI\\')[1].split('VEN_')[1].split('&')
            vendor, device = hwid[0], hwid[1].split('DEV_')[1]
            # 3D Video Controller is the driver installed when no suitable driver is found or installed for the given GPU.
            if vendor == vendor_filter and (driver.DeviceClass == 'DISPLAY' or driver.DeviceName == '3D Video Controller'):
                devices += device,
        except AttributeError:
            pass
        except IndexError:
            pass

    if devices == ():
        message()
    for device in devices:
        try:
            gpu = pciids()['10DE'][1][device]
        except KeyError:
            message()

        if dict == type(gpu):
            if log:
                info(f'Detected: {tuple(gpu.values())[0]}')
            return tuple(gpu.values())[0]
        else:
            if log:
                info(f'Detected: {gpu}')
            return gpu

# Detect if the device being used is a laptop or desktop. (Thanks Felipe#5555! :3)


def system_type() -> str:
    type = [system.wmi_property('ChassisTypes').value[0]
            for system in WMI().Win32_SystemEnclosure()][0]
    if type in (8, 9, 10, 11, 12, 14, 18, 21):
        return 'notebook'
    elif type in (3, 4, 5, 6, 7, 15, 16):
        return 'desktop'
    else:
        print(f"{fg.lred}Error: Couldn't detect system type.{eol}")
        error('Couldn\'t detect system type.')
        exit(1)


def get_drives():
    drives = ()
    for drive in WMI().Win32_LogicalDisk():
        drives += f'{drive.DeviceID}\\',
    return drives


def get_installed_driver_version() -> float:
    try:
        query_key = OpenKey(HKEY_LOCAL_MACHINE,
                            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\{B2FE1952-0186-46C3-BAEC-A80AA35AC5B8}_Display.Driver")
    except FileNotFoundError:
        print(f'{fg.lred}Error: NVIDIA Display Driver is not installed.{eol}')
        error('NVIDIA Display Driver is not installed.')
        exit(1)
    index = 0
    while True:
        try:
            key, value, _ = EnumValue(query_key, index)
            if key == 'DisplayVersion':
                try:
                    return float(value)
                except ValueError:
                    print(
                        f'{fg.lred}Error: NVIDIA Display Driver is not installed.{eol}')
                    error('NVIDIA Display Driver is not installed.')
                    exit(1)
        except OSError:
            break
        index += 1


def get_archiver():
    drives = get_drives()
    returncode = None
    try:
        for drive in drives:
            for archiver in Path(drive).rglob('*7z.exe'):

                try:
                    info(f'Running: "{archiver}"')
                    returncode = run(archiver, capture_output=True).returncode
                except FileNotFoundError:
                    returncode = None
                except OSError:
                    returncode = None

                if returncode == 0:
                    break
            if returncode == 0:
                break
        info(f'Usable Archiver Found: "{archiver}"')
        return f'"{archiver}"'
    except UnboundLocalError:
        print(f"{fg.lred}Error: Couldn't find a usable archiving program.{eol}")
        error('Couldn\'t find a usable archiving program.')
        exit(1)


def dl_links(version, studio=False, type='dch'):
    links = []
    channel = ''
    BASE_LINK = 'https://international.download.nvidia.com/Windows'
    try:
        float(version)
    except ValueError:
        version = version.split('(')[1].strip(')').strip()

    system = system_type()

    match studio:
        case True: nsd = '-nsd'
        case False: nsd = ''

    match type:
        case 'dch': type = '-dch'
        case 'std': type = ''

    if 'quadro' in str(get_gpu(log=False)).lower():
        channel = 'Quadro_Certified/'
        system = 'quadro-rtx-desktop-notebook'

    for winver in ('win10-win11', 'win10'):
        links.append(
            f'{BASE_LINK}/{channel}{version}/{version}-{system}-{winver}-64bit-international{nsd}{type}-whql.exe')
    return links
