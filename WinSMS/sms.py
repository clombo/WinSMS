import datetime
import sys
import os

sys.path.append(os.path.dirname(__file__))

from XMLBuilder import buildfactory as f

factory = f.xmlfactory()

class WinSMS():

    def __init__(self,username,password,obj):
        self._obj = factory.getBuilder(obj,username,password)
        self._response = None

    def __str__(self):
        return self._obj.ToString()

    def ChangeLogins(self,username,password):
        self._obj.UpdateTagData(User=username,Password=password)

    def response(self):
        return self._response

class send(WinSMS):

    def __init__(self,username,passw):
        super().__init__(username,passw,'send')
        self._CurrMsg = None
        self._numbers = []
        self._FullBody = {}
        #self._CountryCode = '27'

    def SetSchedule(self,date_text): #Make sure date is proper format
        try:
            newdate = datetime.datetime.strptime(date_text,"%Y-%m-%d")
            self._obj.UpdateTagData(Schedule=datetime.datetime.strftime(newdate,"%Y%m%d%H%M"))
        except ValueError:
            pass



    #def SetCountryCode(self,code):
    #    self._CountryCode = code

    def _DataInsert(self):

        if (self._CurrMsg != None) and (len(self._numbers) != 0):

            self._FullBody[self._CurrMsg] = self._numbers
            self._obj.dataIns(self._FullBody)

            self._numbers = []
            self._FullBody = {}
            self.CurrMsg = None

    def sendSMS(self):

        self._DataInsert()
        self._response = self._obj.PostXML()
        return self._response

    def Message(self,message):

        self._DataInsert()
        self._CurrMsg = message


    #Replace flags with kwargs? ,IgnoreCounrtyCode=False
    def AddNumbers(self,*numbers):

        if self._CurrMsg == None:
            #Raise error
            assert('No message added')

        for item in numbers:
            if type(item) in [list,dict]:
                raise TypeError('list/dict not supported')
                self._numbers = []
            else:
                #n = item
                #Make sure to use CountryCode
                #if IgnoreCounrtyCode == False:
                    #n[1] = self._CountryCode

                self._numbers.append(item)


class delete(WinSMS):

    def __init__(self,username,passw):
        super().__init__(username, passw,'delsched')

    def Delete(self,ID,CLI=None):
        print(type(self._obj))
        self._obj.dataIns(ID,CLI)
        self._response = self._obj.PostXML()
        return self._response


class replies(WinSMS):
    def __init__(self,username,passw):
        super().__init__(username, passw,'replies')

    def get(self):
        self._response = self._obj.PostXML()
        return self._response

class batchStatus(WinSMS):
    def __init__(self,username,passw):
        super().__init__(username, passw,'batch')

    def GetStatus(self,ID,CLI=None):
        self._obj.dataIns(ID,CLI)
        self._response = self._obj.PostXML()
        return self._response
