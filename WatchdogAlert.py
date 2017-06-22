# Importing AfricasTalkingGateway module
from africastalking import AfricasTalkingGateway as ATG

class instantMessage():
    # Values of the following variables will be captured from an external class
    def __init__(self, destination, message):
        # Message details
        self.destination = destination
        self.message = message
        # Platform Credentials
        self.profile = ""
        self.key = ""

    try:
        def transmit(self):
            gateway = ATG.AfricasTalkingGateway(self.profile, self.key)
            results = gateway.sendMessage(self.destination, self.message)
    except ATG.AfricasTalkingGatewayException, e:
        print 'Encountered an error while sending: %s ' % str(e)
