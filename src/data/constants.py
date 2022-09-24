# API Link.
API_LINK = 'https://www.nvidia.com/Download/processFind.aspx?psid={psid}&pfid={pfid}&osid=57&lid=1&whql={whql}&ctk=0&dtcid={dtcid}'

# Base Driver Package Components.
BASE_COMPONENTS = ['Display.Driver',
                   'NVI2',
                   'EULA.txt',
                   'ListDevices.txt',
                   'setup.cfg',
                   'setup.exe']

# Setup
SETUP = ('<file name="${{EulaHtmlFile}}"/>',
         '<file name="${{PrivacyPolicyFile}}"/>',
         '<file name="${{FunctionalConsentFile}}"/>')

PRESENTATIONS = ('\t\t<string name="ProgressPresentationUrl"',
                 '\t\t<string name="ProgressPresentationSelectedPackageUrl"')
