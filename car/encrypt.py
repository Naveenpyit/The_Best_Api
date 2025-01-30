import os
from dotenv import load_dotenv # type: ignore
load_dotenv()
API_KEY=os.getenv('API_KEY')

class encryption:
    @staticmethod
    def encrypt_key(data):
        keys = " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890~!@#$%^&*()-_=+[]:;'.,<>/?"

        encrypt_data = []
        for char in data:
            if char in keys:
                index = keys.index(char)
                new_index = (index + 5) % len(keys)
                encrypt_data.append(keys[new_index])
            else:
                encrypt_data.append(char)
        return encrypt_data
        
        