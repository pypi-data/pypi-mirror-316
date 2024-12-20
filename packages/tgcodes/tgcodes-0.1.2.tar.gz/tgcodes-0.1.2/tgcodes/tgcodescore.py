import requests
from .tgctypes import *
from typing import Union

class TGCodesManager:
    
    def __init__(self, 
            access_token: str, 
            auth_metod: Union[AuthViaHeader, AuthViaParameter] = AuthViaHeader):
        """API Client for GatewayApi.

        Args:
            access_token (str): Access token from https://gateway.telegram.org/account/api
            auth_metod (Union[AuthViaHeader, AuthViaParameter], optional): Method that will be used for auth. Defaults to AuthViaHeader.
        """
        self.auth = auth_metod(access_token)
    
    def sendVerificationMessage(self, 
            phone_number: int, 
            request_id: str | None = None, 
            sender_username: str | None = None, 
            code: str | None = None, 
            code_length: int | None = None,
            callback_url: str | None = None,
            payload: str | None = None,
            ttl: int | None = None):
        
        """
        Sends a verification message to a user.

        Args:
            phone_number (int): The phone number to which the verification code was sent, in the E.164 format.
            request_id (str, optional): Unique identifier of the verification request. Defaults to None.
            sender_username (str, optional): Username of the sender. Defaults to None.
            code (str, optional): Verification code. Defaults to None.
            code_length (int, optional): Verification code length. Defaults to None.
            callback_url (str, optional): URL that will be sent to a callback to update the status of the verification request. Defaults to None.
            payload (str, optional): Custom payload that will be sent to a callback to update the status of the verification request. Defaults to None.
            ttl (int, optional): Time to live of the verification message. Defaults to None.

        Returns:
            RequestStatus: Status of the verification request.
        """

        tojson = self.auth.tojson
        toheaders = self.auth.toheaders
        toparams = self.auth.toparameters
        
        js = {
            'phone_number': phone_number,
            'request_id': request_id,
            'sender_username': sender_username,
            'code': code,
            'code_length': code_length,
            'callback_url': callback_url,
            'payload': payload,
            'ttl': ttl
        }
        for key, value in js.copy().items():
            if value == None:
                js.pop(key)
        
        tojson.update(js)
        
        response = requests.post('https://gatewayapi.telegram.org/sendVerificationMessage', json=tojson, headers=toheaders, params=toparams)

        return RequestStatus(response)

    def checkSendAbility(self, phone_number: int):
        
        """
        Checks the ability to send a verification message to a specified phone number.

        Args:
            phone_number (int): The phone number to check the send ability for, in the E.164 format.

        Returns:
            RequestStatus: The status of the send ability check request.
        """

        
        
        tojson = self.auth.tojson
        toheaders = self.auth.toheaders
        toparams = self.auth.toparameters
        tojson['phone_number'] = phone_number
        
        response = requests.post('https://gatewayapi.telegram.org/checkSendAbility', json=tojson, headers=toheaders, params=toparams)
        
        return RequestStatus(response)
    
    def checkVerificationStatus(self, request_id: str):
        
        """
        Checks the verification status of a verification message request.

        Args:
            request_id (str): Unique identifier of the verification request.

        Returns:
            RequestStatus: The status of the verification request.
        """
        
        tojson = self.auth.tojson
        toheaders = self.auth.toheaders
        toparams = self.auth.toparameters
        tojson['request_id'] = request_id
        
        response = requests.post('https://gatewayapi.telegram.org/checkVerificationStatus', json=tojson, headers=toheaders, params=toparams)
        
        return RequestStatus(response)
    
    def revokeVerificationMessage(self, request_id: str):
        
        """
        Revokes a verification message request.

        Args:
            request_id (str): Unique identifier of the verification request.

        Returns:
            RequestStatus: The status of the revocation request.
        """
        
        tojson = self.auth.tojson
        toheaders = self.auth.toheaders
        toparams = self.auth.toparameters
        tojson['request_id'] = request_id
        
        response = requests.post('https://gatewayapi.telegram.org/revokeVerificationMessage', json=tojson, headers=toheaders, params=toparams)
        
        return RequestStatus(response)