# mpesa-paybill-confirmation-post-request

This project simulates C2BPaymenConfirmationRequest message from M-Pesa to Broker 

Installation
=====================
$ pip install -r requirements.txt

Usage
=====================
<b>Listener.py</b> acts as a server application that waits for 
soap xml request and process it
<b>ClientPost.py</b> Sends C2BPaymenConfirmationRequest message to the listener


