import ssl
import urllib

from suds.transport.https import HttpAuthenticated
from suds.client import Client

from suds.xsd.doctor import Import
from suds.xsd.doctor import ImportDoctor


class AXL(object):

    def __init__(self, username, password, wsdl, cucm, cucm_version):
        """
        :param username: axl username
        :param password: axl password
        :param wsdl: wsdl file location
        :param cucm: UCM IP address
        :param cucm_version: UCM version

        example usage:
        >>> from axl.foley import AXL
        >>> wsdl = 'file:///path/to/wsdl/axlsqltoolkit/schema/10.5/AXLAPI.wsdl'
        >>> ucm = AXL('axl_user', 'axl_pass' wsdl, '192.168.200.10')
        """
        self.username = username
        self.password = password
        self.wsdl = wsdl
        self.cucm = cucm
        self.cucm_version = cucm_version

        tns = 'http://schemas.cisco.com/ast/soap/'
        imp = Import('http://schemas.xmlsoap.org/soap/encoding/', 'http://schemas.xmlsoap.org/soap/encoding/')
        imp.filter.add(tns)

        t = HttpAuthenticated(username=self.username, password=self.password)
        t.handler = urllib.request.HTTPBasicAuthHandler(t.pm)
        
        ssl_def_context = ssl.create_default_context()
        ssl_def_context.check_hostname = False
        ssl_def_context.verify_mode = ssl.CERT_NONE
        if float(cucm_version) <= 8.5:
            ssl_def_context.set_ciphers('HIGH:!DH:!aNULL')

        t1 = urllib.request.HTTPSHandler(context=ssl_def_context)
        t.urlopener = urllib.request.build_opener(t.handler, t1)

        self.client = Client(self.wsdl, location='https://{0}:8443/axl/'.format(cucm), faults=False, plugins=[ImportDoctor(imp)], transport=t)

    def listProcessNodes(self):
        resp = self.client.service.listProcessNode({'name': '%', 'processNodeRole': 'CUCM Voice/Video'}, returnedTags={'name': ''})
        result = {
            'success': False,
            'response': '',
            'error': '',
        }
        if resp[0] == 200:
            result['success'] = True
            subs = []
            nodes = resp[1]['return']['processNode']
            
            # only return call processing nodes and not the enterprisewidedata node
            for node in nodes:
                    if node.name != 'EnterpriseWideData':
                        subs.append(node.name)
            result['response'] = subs
            return result
        elif resp[0] == 500 and 'was not found' in resp[1].faultstring:
            result['response'] = 'Location: {0} not found'.format(**args)
            result['error'] = resp[1].faultstring
            return result
        else:
            result['response'] = 'Unknown error'
            result['error'] = resp[1].faultstring
            return result