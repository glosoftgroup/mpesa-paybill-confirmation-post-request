import requests
#file = 'test234.xml'
file = 'confirmation.xml'
xml = open(file,'r')

headers = {'Content-Type': 'application/xml'}
#r = requests.post("http://127.0.0.1:5000", data=xml.read(), headers=headers)
r = requests.post("http://127.0.0.1:8000/payment/", data=xml.read(), headers=headers)

print (r.text)
