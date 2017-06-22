#!flask/bin/python
from flask import Flask, request
# import pymysql
import os
import xml.etree.ElementTree as ET
# import csv
from watchdog import dbCon, xmrVED, xmrCED, csvCr
from WatchdogAlert import instantMessage

# ----------------------------------------------------------------------------------------------------------------
# app defines the listening function. The modules listens for any HTTP communication through port 5000
app = Flask(__name__)

@app.route('/', methods=['POST'])

def result():
    try:
        content = request.data
        root = ET.fromstring(content)
        responseVl = ''

    except:
        return "Invalid Request"
        exit()


    for child in root.find('{http://schemas.xmlsoap.org/soap/envelope/}Body'):
        if child.tag == '{http://cps.huawei.com/cpsinterface/c2bpayment}C2BPaymentValidationRequest':
            '''
            This code section defines the process that follows during a Transaction Validation Process
            Once a Transaction validation message is received, a Bill Reference Number value is extracted and
            looked up in a members database. This helps validate the existence of the member within the club.
            '''
            refNumber = child.find('BillRefNumber').text
            transID = child.find('TransID').text
            phnNumber = child.find('MSISDN').text

            responseVl= '+'+phnNumber+'+'+transID
		

            #dv = dbCon(refNumber)

            '''
            if dv.lkUP():
                # This part is as a result of a Return True in the dbCon.lkUP()
                pR = xmrVED('0', 'Service processing successful', transID)
                responseVl= pR.Edit()

            else:
                # This part is as a result of a Return False in the dbCon.lkUP()
                pR = xmrVED('C2B00012', 'Invalid Account Number', transID)
                responseVl = pR.Edit()

            '''

        elif child.tag == '{http://cps.huawei.com/cpsinterface/c2bpayment}C2BPaymentConfirmationRequest':
            # This code section defines the process that follows during a Transaction Confirmation Process
            # Once a confirmation message is received, the information is extracted from the received xml message
            # and dumped into a csv file


            csvCreator = csvCr(content)
            cR = csvCreator.prCre()
            csXm = xmrCED(cR)
            #responseVl = csXm.Edit()

            #route = instantMessage()

    return responseVl


# ------------------------------------------------------------------------------------------------------------------
# This here is the main function()
if __name__ == '__main__':
    app.run(debug=True)