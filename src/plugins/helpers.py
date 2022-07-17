from urllib.request import urlopen
from xml.etree import ElementTree

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

# Parse the GPU List XML file into a dictionary.

def gpus() -> dict:
    response = {}
    xml = ElementTree.parse(urlopen(
        'https://www.nvidia.com/Download/API/lookupValueSearch.aspx?TypeID=3')).getroot()
    for index, tag in enumerate(xml.findall('LookupValues/LookupValue')):
        response[tag[0].text] = {'PSID': str(index), 'PFID': tag[1].text}
    return response