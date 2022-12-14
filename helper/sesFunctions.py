import boto3
import logging
import configparser

logger = logging.getLogger()
logger.setLevel(logging.INFO)

client = boto3.client('ses')

class SESHelper:

    # Function responsible to send the Email
    def send_email(self, email_id, message):
        config = configparser.ConfigParser()
        config.readfp(open(r'config.conf'))
        from_email = config.get('Configuration', 'from_email')

        send_email = client.send_email(
            Source= from_email,
            Destination={
                'ToAddresses': [email_id],                
            },
            Message={
                'Subject': { 'Data': 'Reminder!!'},
                'Body': {
                    'Text': {'Data': message},                    
                }
            },            
        )

        logger.info(send_email)
        return send_email['ResponseMetadata']['HTTPStatusCode']

    # Function to get the list of verified Email Ids From SES Sandbox
    def list_verified_emails(self):
        list_identities = client.list_identities(
            IdentityType='EmailAddress'
        )['Identities']
        logger.info(list_identities)
        return list_identities

    # Function to send the verification Email
    def send_verification_email(self, email_id):
        response = client.verify_email_identity(
            EmailAddress=email_id
        )
        logger.info(response)
        return response['ResponseMetadata']['HTTPStatusCode']
        

