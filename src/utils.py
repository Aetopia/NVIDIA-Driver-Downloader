from wmi import WMI
from fnmatch import fnmatch
from urllib.request import urlopen
from sys import exit

# Get PSID and PFID of the installed NVIDIA GPU.
def detect_gpu() -> tuple:
    for GPU in WMI().Win32_VideoController():
        gpu = GPU.wmi_property('Caption').value
        if 'nvidia' in gpu.lower():
            if 'geforce' in gpu.lower():
                gpu = gpu.split("NVIDIA")[1].strip()
            break
        else:
            print('NVDDL is currently running in fallback mode.')
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