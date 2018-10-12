[![published](https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-published.svg)](https://developer.cisco.com/codeexchange/github/repo/levensailor/py-cisco-ris)

# py-cisco-ris

Uses Realtime Information Service (RIS) to capture registration status of Cisco IP Phones on CUCM
https://developer.cisco.com/docs/sxml/#risport70-api-reference

#### For a full example - see example.py

```bash
pip install py-cisco-ris
```

#### import RIS, (and AXL if you want the script to find your call processors for you)
```py
from axlhelper import AXL
from py-cisco-ris import RIS
```

#### specify your CUCM details, including a RIS and AXL user if these are different
```py
cucm = os.getenv('cucm', '10.10.10.10')
version = os.getenv('version', '11.5')
axluser = os.getenv('axluser', 'axladmin')
axlpass = os.getenv('axlpass', 'p@ssw0rd')
risuser = os.getenv('risuser', 'axladmin')
rispass = os.getenv('rispass', 'p@ssw0rd')
```

#### instanciate your RIS and AXL objects
```py
axl = AXL(username=axluser,password=axlpass,wsdl=wsdl,cucm=cucm,cucm_version=version)
ris = RIS(username=risuser,password=rispass,cucm=cucm,cucm_version=version)
```

#### input an array of phones and run the following to output registrations

```py
phones = ['SEPF8A5C59E0F1C', 'SEP1CDEA78380DE', 'SEP01CD4EF58980']

getSubs()
groups = limit(phones)
for group in groups:
    registered = checkRegistration(group, subs)
    print(registered['TimeStamp'])
```
