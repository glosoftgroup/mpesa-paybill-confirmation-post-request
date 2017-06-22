import pymysql
import os
import xml.etree.ElementTree as ET
import csv

# ---------------------------------------------------------------------------------------------------------------
# This point opens up a connection string to the MySql Database
class dbCon():
    def __init__(self, RefVl):
        self.RefVl = int(RefVl)     # ***At this point Check the datatype of the MemberID as defined within DB***
        self.sqCon = pymysql.connect("localhost", "root", "CodeByte29", "testdb")
        self.cursor = self.sqCon.cursor()
        self.cursor.execute("SELECT id FROM users")
        self.rows = self.cursor.fetchall()
        # self.blVal = False

    def lkUP(self):
        blVal = False

        for item in self.rows:
            if item[0] == self.RefVl:
                blVal = True
            # print item

        return blVal

# -----------------------------------------------------------------------------------------------------------------
# This point opens up the Validation response xml messages and prepares them for communication
class xmrVED():
    def __init__(self, rsCode, rsDesc, rsID):
        self.rsCode = rsCode
        self.rsDesc = rsDesc
        self.rsID = rsID
        self.base = '/mnt/4054A6C354A6BAD4/Bionic/Projects/Python Projects/Watchdog_REST_API/Responses/ValidationResponse.xml'

    # This method will edit the existing ValidationResponse file to match new information
    def Edit(self):
        nwXml = ET.parse(self.base)
        ET.register_namespace('soapenv', 'http://schemas.xmlsoap.org/soap/envelope/')
        ET.register_namespace('c2b', 'http://cps.huawei.com/cpsinterface/c2bpayment')
        root = nwXml.getroot()

        # This point looks for the associated tags and sets the new values
        for item in root.iter('ResultCode'):
            item.text = self.rsCode
        for item in root.iter('ResultDesc'):
            item.text = self.rsDesc
        for item in root.iter('ThirdPartyTransID'):
            item.text = self.rsID

        # The following point modifies the ValidationResponse file with new information
        nwXml.write(self.base)
        # This point converts the modified XML file into string
        xmlString = ET.tostring(root, encoding='utf8', method='xml')

        return xmlString



# ------------------------------------------------------------------------------------------------------------------
# This point is responsible for building a csv file from the extracted transaction data.
class csvCr():
    def __init__(self, xmlString):
        self.xmlString = xmlString
        self.rootInfo = []

    def prCre(self):
        root = ET.fromstring(self.xmlString)
        for childVl in root.find('{http://schemas.xmlsoap.org/soap/envelope/}Body'):
            refNumber = childVl.find('BillRefNumber').text
            self.rootInfo.append(refNumber)
            transTime = childVl.find('TransTime').text
            transAmt = childVl.find('TransAmount').text
            self.rootInfo.append(transAmt)
            self.rootInfo.append('ADMIN')
            self.rootInfo.append('DEBIT')
            self.rootInfo.append('DEBIT')
            transID = childVl.find('TransID').text
            self.rootInfo.append(transID)
            fileDump = (str(refNumber) + str(transTime) + '.csv')
            writing = open(fileDump, 'w')
            os.chmod(fileDump, 0777)
            csvWriter = csv.writer(writing)
            csvWriter.writerow(self.rootInfo)
            print ':- Information embedded in CSV File: ' + fileDump
            writing.close()
            print '-------------------------------------------------'
            print '-------------------------------------------------'

        return transID


# ------------------------------------------------------------------------------------------------------------------
# This point on the other hand opens up the Confirmation Response and prepares it for transmission.
class xmrCED():
    def __init__(self, trCodeID):
        self.trCodeID = trCodeID
        self.base = '/mnt/4054A6C354A6BAD4/Bionic/Projects/Python Projects/Watchdog_REST_API/Responses/ConfirmationResponse.xml'

    def Edit(self):
        nwxml = ET.parse(self.base)
        ET.register_namespace('soapenv', 'http://schemas.xmlsoap.org/soap/envelope/')
        ET.register_namespace('c2b', 'http://cps.huawei.com/cpsinterface/c2bpayment')
        root = nwxml.getroot()

        # This point will look for the associated tag and set the new value.
        for item in root.find('{http://schemas.xmlsoap.org/soap/envelope/}Body'):
            item.text = 'C2B Payment Transaction '+ str(self.trCodeID) +' result received.'

        # The following line will make the actual changes within the xml file
        nwxml.write(self.base)
        # This line will parse the file into a string ready for returning
        xmlString = ET.tostring(root, encoding='utf8', method='xml')

        return xmlString