import os
import sys
import time

'''
import RIS for Realtime Information Service 
import AXL for convenience to lookup call processing nodes
'''

from axlhelper import AXL
from ris import RIS

'''
Pull in environment variables or use defaults, which you can edit here
'''

cucm = os.getenv('cucm', '10.10.10.10')
version = os.getenv('version', '11.5')
axluser = os.getenv('axluser', 'axladmin')
axlpass = os.getenv('axlpass', 'p@ss0wrd')
risuser = os.getenv('risuser', 'axladmin')
rispass = os.getenv('rispass', 'p@ssw0rd')

'''
AXL schema is hosted locally, so this uses the proper WSDL from the specified version
'''
full  = os.path.abspath(os.path.dirname('.'))
sys.path.append(full)
wsdl = 'file://'+full+'/schema/'+version+'/AXLAPI.wsdl'

'''
Setup your objects here
'''
axl = AXL(username=axluser,password=axlpass,wsdl=wsdl,cucm=cucm,cucm_version=version)
ris = RIS(username=risuser,password=rispass,cucm=cucm,cucm_version=version)

'''
You can specify phones here, or use another function to pull phones
'''
phones = ['SEPF8A5C59E0F1C', 'SEP1CDEA78380DE', 'a', 'b', 'b33', 'sdfdsf', 'jljl']

CmSelectionCriteria = {
    "MaxReturnedDevices": "1000",
    "DeviceClass": "Phone",
    "Model": 255,
    "Status": "Registered",
    "NodeName": "",
    "SelectBy": "Name",
    "SelectItems": {
        "item": {
            "Item": ""
        }
    },
    "Protocol": "Any",
    "DownloadStatus": "Any"
}

'''
Use AXL to get all call processing nodes
'''

def getSubs():
    nodes = axl.listProcessNodes()
    if nodes['success']:
        return nodes['response']

'''
Use RIS to lookup phone registrations on every call processing node
This takes an array of phones, up to 1000 at a time, with an API limit of 15/limit or a call every 4 seconds
'''

def checkRegistration(phones, subs):
    for sub in subs:
        CmSelectionCriteria['NodeName'] = sub
        CmSelectionCriteria['SelectItems']['item']['Item'] = ",".join(phones)
        reg = ris.get_devices(**CmSelectionCriteria)
        if reg['success']:
            return reg['response']


'''
Groups phones into sets of 1000 if needed
'''
limit = lambda phones, n=1000: [phones[i:i+n] for i in range(0, len(phones), n)]


subs = getSubs()
groups = limit(phones)
for group in groups:
    registered = checkRegistration(group, subs)

    '''
    Do what  you wish with the return data
    '''
    user = registered['LoginUserId']
    regtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(registered['TimeStamp']))
    for item in registered['IPAddress']:
        ip = item[1][0]['IP']

    for item in registered['LinesStatus']:
        primeline = item[1][0]['DirectoryNumber']
    name = registered['Name']

    print(name)
    print(user)
    print(primeline)
    print(ip)
    print(regtime)