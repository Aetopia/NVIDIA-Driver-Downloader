from tempfile import gettempdir
from nvapi.query import get_driver_vers, get_nv_gpu
from urllib.request import urlopen
from urllib.error import HTTPError
from subprocess import run


def download(ver: float = None, studio=False, std=False, notebook=False, output=gettempdir()) -> None:
    channel, nsd, type = '', '', '-dch'
    plat, quadro = 'desktop', False
    if ver is None:
        vers, quadro = get_driver_vers()
        ver = vers[0]
    else:
        _, _, quadro = get_nv_gpu()

    if studio: nsd = '-nsd'
    if std: type = ''
    if notebook: plat = 'notebook'

    if quadro:
        channel = 'Quadro_Certified/'
        plat = 'quadro-rtx-desktop-notebook'

    output = f'{output}/NVIDIA - {ver}.exe'

    for winver in ('win10-win11', 'win10'):
        link = f'https://international.download.nvidia.com/Windows/{channel}{ver}/{ver}-{plat}-{winver}-64bit-international{nsd}{type}-whql.exe'
        try:
            if urlopen(link).getcode() == 200:
                run(f'curl -o "{output}" "{link}"')
                return
        except HTTPError:
            pass
    raise Exception('Couldn\'t find a valid download link.')
