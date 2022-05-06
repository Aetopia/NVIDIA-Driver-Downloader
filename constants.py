STUDIO_DESKTOP_LINK = (
    'https://international.download.nvidia.com/Windows/{driver_version}/{driver_version}-desktop-win10-win11-64bit-international-nsd-dch-whql.exe',
    'https://international.download.nvidia.com/Windows/{driver_version}/{driver_version}-desktop-win10-64bit-international-nsd-dch-whql.exe'
    )
STUDIO_NOTEBOOK_LINK = (
    'https://international.download.nvidia.com/Windows/{driver_version}/{driver_version}-notebook-win10-win11-64bit-international-nsd-dch-whql.exe',
    'https://international.download.nvidia.com/Windows/{driver_version}/{driver_version}-notebook-win10-64bit-international-nsd-dch-whql.exe'
)

GR_DESKTOP_LINK = (
    'https://international.download.nvidia.com/Windows/{driver_version}/{driver_version}-desktop-win10-win11-64bit-international-dch-whql.exe',
    'https://international.download.nvidia.com/Windows/{driver_version}/{driver_version}-desktop-win10-64bit-international-dch-whql.exe'
    )

GR_NOTEBOOK_LINK = (
    'https://international.download.nvidia.com/Windows/{driver_version}/{driver_version}-notebook-win10-win11-64bit-international-dch-whql.exe',
    'https://international.download.nvidia.com/Windows/{driver_version}/{driver_version}-notebook-win10-64bit-international-dch-whql.exe'
    )

LINK= 'https://www.nvidia.com/Download/processFind.aspx?psid={psid}&pfid={pfid}&osid=57&lid=1&whql={whql}&ctk=0&dtcid=1'
COMPONENTS = 'Display.Driver NVI2 EULA.txt ListDevices.txt GFExperience/*.txt GFExperience/locales GFExperience/EULA.html GFExperience/PrivacyPolicy setup.cfg setup.exe'
REG_KEY = r'reg query "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\{B2FE1952-0186-46C3-BAEC-A80AA35AC5B8}_Display.Driver" /v DisplayVersion'