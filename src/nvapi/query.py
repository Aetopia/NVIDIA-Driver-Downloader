from fnmatch import fnmatch
import nvapi.info as info
from urllib.request import urlopen
import winreg


def get_driver_vers(studio=False, std=False) -> list:
    whql, dtcid, vers = 1, 1, []
    psid, pfid, quadro = get_nv_gpu()
    if studio:
        whql = 4
    if std:
        dtcid = 0

    link = f'https://www.nvidia.com/Download/processFind.aspx?psid={psid}&pfid={pfid}&osid=57&lid=1&whql={whql}&ctk=0&dtcid={dtcid}'

    for line in [_.decode('UTF-8').strip() for _ in urlopen(link)]:
        if fnmatch(line, '<td class="gridItem">*.*</td>'):
            ver = line.split('>')[1].split('<')[0]
            if ver != '':
                try:
                    float(ver)
                except ValueError:
                    ver = ver.split(
                        '(')[1].strip(')').strip()
                vers.append(ver)
    return vers, quadro


def get_nv_gpu() -> list:
    i, nvdvcs = 0, []
    pciids, nvgpus, = info.pciids(), info.nvgpus(),
    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                         'SYSTEM\\CurrentControlSet\\Enum\\PCI')
    while True:
        try:
            hwid = winreg.EnumKey(key, i).split('&')[0:2]
            ven, dev = hwid[0].split('VEN_')[1], hwid[1].split('DEV_')[1]
            try:
                if ven == '10DE':
                    dvc = pciids['10DE'][1][dev]
                    if type(dvc) == dict:
                        dvc = tuple(dvc.values())[0]
                    nvdvcs.append(dvc)
            except KeyError:
                break
            i += 1
        except WindowsError:
            break

    for gpu in nvgpus.keys():
        for dvc in nvdvcs:
            if gpu in dvc:
                quadro = 'quadro' in gpu.lower()
                return nvgpus[gpu]['PSID'], nvgpus[gpu]['PFID'], quadro
