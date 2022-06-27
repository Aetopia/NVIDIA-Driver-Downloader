"""
This file contains WIP and experimental code.

What has been added:
1. Hardware based detection of the GPU.
2. Optimized get_psid_pfid() function.
3. Using PCIIDs to get the GPU name.
"""
from wmi import WMI
from urllib.request import urlopen
from utils import gpus
from textformat import fg, eol
from logging import basicConfig, error, info, warning
from tempfile import gettempdir
"""
NVIDIA Family -> '10DE'
Device Type -> 'DISPLAY'
"""

basicConfig(filename=f'{gettempdir()}/nvddl.log', filemode='w+',
            format='%(levelname)s: %(message)s', level='INFO')

def get_psid_pfid() -> tuple:
    gpu_list = gpus()
    isNVIDIA = True
    detected_gpu = get_gpu()

    for gpu in gpu_list.keys():
        if gpu in detected_gpu:
            return gpu_list[gpu]['PSID'], gpu_list[gpu]['PFID']
    else:
        isNVIDIA = False

    if isNVIDIA is False:
        print(f'{fg.lred}Warning: No NVIDIA GPU detected, using fallback mode.{eol}\n')
        warning('No NVIDIA GPU detected, using fallback mode.')
        return gpu_list['GeForce GTX 1050']['PSID'], gpu_list['GeForce GTX 1050']['PFID']


def get_gpu():
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

    for device in devices:
        try:
            gpu = pciids()['10DE'][1][device]
        except KeyError:
            print(f'{fg.lred}Error: No NVIDIA GPU Detected.{eol}')
            error('No NVIDIA GPU Detected.')
            exit(1)

        if dict == type(gpu):
            info(f'Detected: {tuple(gpu.values())[0]}')
            return tuple(gpu.values())[0]
        else:
            info(f'Detected: {gpu}')
            return gpu


def pciids():
    """
    Parse the PCIIDs file into a dictionary.
    """
    response = {}
    for line in urlopen('https://raw.githubusercontent.com/pciutils/pciids/master/pci.ids').read().decode('UTF-8').splitlines():
        try:
            if line.startswith('#') is False:

                # Devices
                if ('\t') == tuple(line)[0] and ('\t') != tuple(line)[1]:
                    device, device_name = line.strip('\t').split(' ' * 2, 1)
                    response[vendor.upper()][1][device.upper()] = device_name

                # Subvendors + Subdevices + Subsystems
                if ('\t', '\t') == tuple(line)[0:2]:
                    subvendor_subdevice, subsystem_name = line.strip(
                        '\t').strip().split(' ' * 2, 1)
                    try:
                        subvendor, subdevice = subvendor_subdevice.split()
                        response[vendor.upper()][1][subvendor.upper()] = {
                            subdevice.upper(): subsystem_name}
                    except ValueError:
                        response[vendor.upper(
                        )][1][subvendor_subdevice.upper()] = subsystem_name

                # Vendors
                elif ('\t') != tuple(line)[0] and 'C' != tuple(line)[0]:
                    vendor, vendor_name = line.split(' ' * 2, 1)
                    response[vendor.upper()] = [vendor_name, {}]

        except IndexError:
            pass
    return response
