#imports
from xml.etree.ElementTree import Element,tostring,SubElement,fromstring
from xml.dom import minidom
from xml.etree import ElementTree
import datetime
import requests
from xmljson import parker
from json import dumps

#URL constants
WINSMS_SENDSMS_URL = 'http://www.winsms.co.za/api/XMLSendSMSMulti.asp'
WINSMS_DELSCHED_URL = 'http://www.winsms.co.za/api/XMLDeleteScheduled.asp'
WINSMS_BATCHSTAT_URL = 'http://www.winsms.co.za/api/XMLGetStatus.asp'
WINSMS_GETREPLIES_URL = 'http://www.winsms.co.za/api/XMLGetReplies.asp'

#Default xml class
class DefaultXML():
    """docstring for DefaultXML."""

    def __init__(self,username,password,tag,URL):
        #Root tag to be used, pending on class called
        self._root = Element(tag)
        #username tag to Root
        self._username = SubElement(self._root,'User')
        self._username.text = username
        #password tag to Root
        self._passw = SubElement(self._root,'Password')
        self._passw.text = password
        self._URL = URL

    def ToString(self):
        xml = self._XMLDoc()
        return xml


    def _XMLDoc(self):
        #Do pretty print here
        roughString = ElementTree.tostring(self._root,'utf-8')
        reparsed = minidom.parseString(roughString)
        return reparsed.toprettyxml(indent="    ")

    def PostXML(self):
        #post XML and get response
        headers = {'Content-Type' : 'application/xml'}
        resp = requests.post(self._URL,data=ElementTree.tostring(self._root, method='xml'),headers=headers)
        self._DelChild()
        return dumps(parker.data(fromstring(resp.text), preserve_root=True),indent=4)

    def UpdateTagData(self,**kwargs):
        for child in self._root:
            if child.tag in kwargs.keys():
                child.text = kwargs[child.tag]

    def _DelChild(self):
        for child in self._root:
            if child.tag in ['Messages','MessageIDs']:
                self._root.remove(child)


#Send SMS (bulk) xml class
class SendXML(DefaultXML):
    """docstring for SendXML."""

    def __init__(self,username,password):
        super().__init__(username,password,'WinSMS_Multi_Message',WINSMS_SENDSMS_URL)

        #Schedule data
        self._schedule = datetime.datetime.now().strftime("%Y%m%d%H%M")
        self._schedtag = SubElement(self._root,'Schedule')
        self._schedtag.text = self._schedule


    #Data insert
    def dataIns(self,data):
        #Messages tag
        #self._msgstag = SubElement(self._root,'Messages')
        toptag = SubElement(self._root,'Messages')

        for msg,nbrs in data.items():

            msgtag = SubElement(toptag,'Message')
            nbrstag = SubElement(msgtag,'Numbers')

            msgtxt = SubElement(msgtag,'MessageText')
            msgtxt.text = msg

            for item in nbrs:
                nbrtag = SubElement(nbrstag,'Number')
                nbrtag.text = item




#Batch Status xml class
class BatchStatusXML(DefaultXML):
    """docstring for BatchStatusXML."""

    def __init__(self,username,password):
        super().__init__(username,password,'WinSMS_StatusRequest',WINSMS_BATCHSTAT_URL)

        #Unique tag to Batch Status
        self._msgidtag = SubElement(self._root,'MessageIDs')

    #Data insert
    def dataIns(self,ID,CLI):

            msgidstag = SubElement(self._msgidtag,'MessageID')

            msgid = SubElement(msgidstag,'ID')
            msgcli = SubElement(msgidstag,'CLI')

            msgid.text = ID
            msgcli.text = CLI

#Replies xml class
class RepliesXML(DefaultXML):
    """docstring for RepliesXML."""

    def __init__(self,username,password):
        super().__init__(username,password,'WinSMS_Replies',WINSMS_GETREPLIES_URL)

#Delete schedule xml class
class DelSchedXML(DefaultXML):
    """docstring for DelSchedXML."""

    def __init__(self,username,password):
        super().__init__(username,password,'WinSMS_DeleteScheduled',WINSMS_DELSCHED_URL)

        #Unique tag to Delete
        self._msgidtag = SubElement(self._root,'MessageIDs')

    #Data insert
    def dataIns(self,ID,CLI):

        msgidstag = SubElement(self._msgidtag,'MessageID')

        msgid = SubElement(msgidstag,'ID')
        msgcli = SubElement(msgidstag,'CLI')

        msgid.text = ID
        msgcli.text = CLI
