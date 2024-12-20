import requests

class DeliveryStatus:
    
    def __init__(self, response: requests.Response):
        """
        Represents the delivery status of a message.

        Attributes:
            status (str): The current status of the message. This can be one of the following:
             - 'sent': The message has been sent to the recipient's device(s).
             - 'read': The message has been read by the recipient.
             - 'revoked': The message has been revoked.
             
            updated_at (int): The timestamp (in seconds since epoch) when the status was last updated.
        """
        
        content = response.json()['result']
        self.status = content['delivery_status']['status']
        self.updated_at = content['delivery_status']['updated_at']
        
class VerificationStatus:
    
    def __init__(self, response: requests.Response):
        """
        Represents the verification status of a message.

        Attributes:
            status (str): The current status of the verification process. This can be one of the following:
             - 'pending': The verification process is still in progress.
             - 'approved': The verification process has been approved.
             - 'rejected': The verification process has been rejected.
             - 'expired': The verification process has expired.
            
            updated_at (int): The timestamp for this particular status. Represents the time when the status was last updated.
            code_entered (str): Optional. The code entered by the user.
        """
        
        content = response.json()['result']
        self.status = content['verification_status']['status']
        self.updated_at = content['verification_status']['updated_at']
        self.code_entered = content['verification_status']['code_entered']

class RequestStatus:
    
    def __init__(self, response: requests.Response):
        """This object represents the status of a verification message request.

        Args:
            response (requests.Response): Response from API
            
        Attributes:
            request_id (str): Unique identifier of the verification request.
            phone_number (str): The phone number to which the verification code was sent, in the E.164 format.
            request_cost (float): Total request cost incurred by either checkSendAbility or sendVerificationMessage.
            remaining_balance (float): Optional. Remaining balance in credits. Returned only in response to a request that incurs a charge.
            delivery_status (tgctypes.DeliveryStatus): Optional. The current message delivery status. Returned only if a verification message was sent to the user.
            verification_status (tgctypes.VerificationStatus): Optional. The current status of the verification process.
            payload (str): Optional. Custom payload if it was provided in the request, 0-256 bytes.
        """
        
        content = response.json()['result']
        
        if 'error' in content.keys():
            raise Exception(content['error']) if 'error' in content.keys() else None
        self.request_id = content['request_id'] if 'request_id' in content.keys() else None
        self.phone_number = content['phone_number'] if 'phone_number' in content.keys() else None
        self.request_cost = content['request_cost'] if 'request_cost' in content.keys() else None
        self.remaining_balance = content['remaining_balance'] if 'remaining_balance' in content.keys() else None
        self.delivery_status = DeliveryStatus(response) if 'delivery_status' in content.keys() else None
        self.verification_status = VerificationStatus(response) if 'verification_status' in content.keys() else None
        self.payload = content['payload'] if 'payload' in content.keys() else None
        
class AuthViaHeader:
    
    def __init__(self, access_token: str):
        """Authorization via Header in HTTP request.

        Args:
            access_token (str): acces_token from https://gateway.telegram.org/account/api
            
        Attributes:
            toheaders (dict): Keys/values that will be added to headers
            toparameters (dict): Keys/values that will be added to parameters
            tojson (dict): Keys/values that will be added to json
        """
        
        self.toheaders = {'Authorization' : f'Bearer {access_token}'}
        self.toparameters = {}
        self.tojson = {}
        
class AuthViaParameter:
    
    def __init__(self, access_token: str):
        """Authorization via Header in HTTP request.

        Args:
            access_token (str): acces_token from https://gateway.telegram.org/account/api
            
        Attributes:
            toheaders (dict): Keys/values that will be added to headers
            toparameters (dict): Keys/values that will be added to parameters
            tojson (dict): Keys/values that will be added to json
        """
        
        self.toheaders = {}
        self.toparameters = {"access_token" : access_token}
        self.tojson = {}