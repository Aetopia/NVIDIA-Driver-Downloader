from wmi import WMI
from winreg import HKEY_LOCAL_MACHINE, OpenKey, EnumKey, EnumValue
from logging import basicConfig, error
from plugins.files import gpus, pciids
from tempfile import gettempdir

basicConfig(filename=f'{gettempdir()}/nvddl.log', filemode='w+',
            format='%(levelname)s: %(message)s', level='INFO')

# Get NVIDIA Devices.


def get_devices():
    devices = []
    index = 0
    key = OpenKey(HKEY_LOCAL_MACHINE, 'SYSTEM\\CurrentControlSet\\Enum\\PCI')
    while True:
        try:
            hwid = EnumKey(key, index).split('&')[0:2]
            ven, dev = hwid[0].split('VEN_')[1], hwid[1].split('DEV_')[1]
            if ven == '10DE':
                try:
                    device = pciids().read()['10DE'][1][dev]
                except KeyError:
                    break

                if dict == type(device):
                    devices.append(tuple(device.values())[0])
                else:
                    devices.append(device)
            index += 1
        except WindowsError:
            break
    if devices != []:
        return devices
    else:
        error('No NVIDIA devices found.')
        raise Exception('No NVIDIA devices found.')

# Get NVIDIA GPU.


def get_gpu() -> tuple:
    gpu_list = gpus().read()
    devices = get_devices()

    for gpu in gpu_list.keys():
        for device in devices:
            if gpu in device:
                return gpu, gpu_list[gpu]['PSID'], gpu_list[gpu]['PFID']

# Detect if the device being used is a laptop or desktop. (Thanks Felipe#5555! :3)


def system_type() -> str:
    type = WMI().Win32_SystemEnclosure()[0].ChassisTypes[0]
    if type in (8, 9, 10, 11, 12, 14, 18, 21):
        return 'notebook'
    elif type in (3, 4, 5, 6, 7, 15, 16):
        return 'desktop'
    else:
        error('Couldn\'t detect system type.')
        raise Exception('Couldn\'t detect system type.')

def get_installed_driver_version() -> float:
    try:
        query_key = OpenKey(HKEY_LOCAL_MACHINE,
                            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\{B2FE1952-0186-46C3-BAEC-A80AA35AC5B8}_Display.Driver")
    except FileNotFoundError:
        error('NVIDIA Display Driver is not installed.')
        raise Exception('NVIDIA Display Driver is not installed.')

    index = 0
    while True:
        try:
            key, value, _ = EnumValue(query_key, index)
            if key == 'DisplayVersion':
                try:
                    return float(value)
                except ValueError:
                    error('NVIDIA Display Driver is not installed.')
                    raise Exception('NVIDIA Display Driver is not installed.')
        except OSError:
            break
        index += 1


def dl_links(version, studio=False, type='dch'):
    links = []
    channel = ''
    BASE_LINK = 'https://international.download.nvidia.com/Windows'

    system = system_type()

    match studio:
        case True: nsd = '-nsd'
        case False: nsd = ''

    match type:
        case 'dch': type = '-dch'
        case 'std': type = ''

    if 'quadro' in get_gpu()[0].lower():
        channel = 'Quadro_Certified/'
        system = 'quadro-rtx-desktop-notebook'

    for winver in ('win10-win11', 'win10'):
        links.append(
            f'{BASE_LINK}/{channel}{version}/{version}-{system}-{winver}-64bit-international{nsd}{type}-whql.exe')
    return links
