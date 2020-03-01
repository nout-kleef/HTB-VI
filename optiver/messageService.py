from secrets import TWILLIO_AUTH_TOKEN, TWILLIO_ACCOUNT_SID
from twilio.rest import Client

class MessageService():        
    def __init__(self, number_to_inform):
        self.client = Client(TWILLIO_ACCOUNT_SID, TWILLIO_AUTH_TOKEN)
        self.number_to_inform = number_to_inform
        self.sendInitMessage()
        
    def sendInitMessage(self):
        message = self.client.messages.create(from_='+12058462931',to=self.number_to_inform,body="Hello! Automated trading system is started!")
        print(message.sid)

    def sendMessageUpdate(self, percentage_profit):  
        print('Sending Message')      
        message = self.client.messages.create(body="Hello! I just made: {0} percentage profit!".format(percentage_profit),from_='+12058462931',to=self.number_to_inform)
        print(message.sid)
       




      