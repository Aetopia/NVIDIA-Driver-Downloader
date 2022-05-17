from wmi import WMI
from fnmatch import fnmatch
from urllib.request import urlopen
from sys import exit

# Get PSID and PFID of the installed NVIDIA GPU.
def get_gpu() -> tuple:
    gpu_list = gpus()
    IS_NOT_NVIDIA = False
    for detected_gpus in WMI().Win32_VideoController():
        detected_gpu = detected_gpus.wmi_property('Caption').value
        if 'nvidia' in detected_gpu.lower():
            for gpu in gpu_list.keys():
                if gpu in detected_gpu:
                    return gpu_list[gpu]['PSID'], gpu_list[gpu]['PFID']
        else: IS_NOT_NVIDIA = True
    if IS_NOT_NVIDIA: 
        print('No NVIDIA GPU Detected: Using Fallback Mode.')
        return gpu_list['GeForce GTX 1050' ]['PSID'], gpu_list['GeForce GTX 1050' ]['PFID']
    
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

# Detect if the device being used is a laptop or desktop. (Thanks Felipe#5555! :3)
def system_type() -> str:
    type = [system.wmi_property('ChassisTypes').value[0] for system in WMI().Win32_SystemEnclosure()][0]
    if type in (8, 9, 10, 11, 12, 14, 18, 21):
        return 'laptop'
    elif type in (3, 4, 5, 6, 7, 15, 16):
        return 'desktop'
    else:
        print("Error: Couldn't detect system type.")
        exit()                  