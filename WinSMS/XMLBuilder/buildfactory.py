import sys
import os

sys.path.append(os.path.dirname(__file__))

from builder import SendXML,BatchStatusXML,DelSchedXML,RepliesXML

class xmlfactory:

    @staticmethod
    def getBuilder(type,username,password):

        #Send XML class
        if type.upper() == 'SEND':
            return SendXML(username,password)
        #Delete XML class
        if type.upper() == 'DELSCHED':
            return DelSchedXML(username, password)
        #Batch Status XML class
        if type.upper() == 'BATCH':
            return BatchStatusXML(username, password)
        #Replies XML class
        if type.upper() == 'REPLIES':
            return RepliesXML(username, password)

        assert 0, 'Could not find xml builder: '+type
