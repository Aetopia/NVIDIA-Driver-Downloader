from os import path
from urllib.request import urlopen, urlretrieve
from xml.etree import ElementTree
from tempfile import gettempdir
from ast import literal_eval

class pciids:
    def __init__(self):
        file = f'{gettempdir()}/pciids.txt'
        self.file = file

    def fetch(self):
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

        with open(self.file, 'w', encoding='UTF-8') as f:
            f.write(str(response))
    
    def read(self):
        if path.exists(self.file) is False:
            self.fetch()

        with open(self.file, 'r', encoding='UTF-8') as f:
            return literal_eval(f.read())

# Parse the GPU List XML file into a dictionary.

class gpus():
    def __init__(self):
        file = f'{gettempdir()}/gpus.txt'
        self.file = file

    def fetch(self):
        response = {}
        xml = ElementTree.parse(urlopen(
            'https://www.nvidia.com/Download/API/lookupValueSearch.aspx?TypeID=3')).getroot()
        for index, tag in enumerate(xml.findall('LookupValues/LookupValue')):
            response[tag[0].text] = {'PSID': str(index), 'PFID': tag[1].text}

        with open(self.file, 'w', encoding='UTF-8') as f:
            f.write(str(response))
    
    def read(self):
        if path.exists(self.file) is False:
            self.fetch()
        with open(self.file, 'r', encoding='UTF-8') as f:
            return literal_eval(f.read())

def archiver():
    link = 'https://www.7-zip.org/a/7zr.exe'
    file = f'{gettempdir()}/7zr.exe'
    if path.exists(file) is False:
        urlretrieve(link, file)
    return file