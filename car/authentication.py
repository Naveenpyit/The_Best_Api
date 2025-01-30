from rest_framework.authentication import BaseAuthentication # type: ignore
from rest_framework.exceptions import AuthenticationFailed # type: ignore
from .encrypt import encryption
import os
from dotenv import load_dotenv # type: ignore
load_dotenv()

API_KEY=os.getenv('API_KEY')
class apikeycheck(BaseAuthentication):
    def authenticate(self,request):
        api_key=request.headers.get('api-key')
        
        secret_key=''.join(encryption.encrypt_key(API_KEY))
        print(secret_key)

        if not api_key:
            raise AuthenticationFailed("Key Must Required")
        if api_key !=secret_key:
            raise AuthenticationFailed("Invalid Key!")
        return None
