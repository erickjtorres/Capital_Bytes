from twilio.rest import Client
import time

account_sid = 'mock_sid'
auth_token = 'mock_auth'



client = Client(account_sid, auth_token)

service = client.verify.services.create(
                                     friendly_name='My Service'
                                 )


def subscribe_to_twilio(phoneNumber: str, companyName:str):
    verification = client.verify \
                        .services(service.sid) \
                        .verifications \
                        .create(to=phoneNumber, channel='sms')
    
    verification = client.verify \
                        .services(service.sid) \
                        .verifications(verification.sid) \
                        .update(status='approved')


    message = client.messages.create(
                                body='Thank you for subscribing to our feed. You will be receiving important updates about {0} very soon'.format(companyName),
                                from_='+13304765726',
                                to=phoneNumber
                            )
