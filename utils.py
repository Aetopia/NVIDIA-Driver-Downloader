from wmi import WMI
from fnmatch import fnmatch
from urllib.request import urlopen

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