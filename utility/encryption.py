from cryptography.fernet import Fernet
import base64


class Encrptor:
    def __init__(self,*args, **kwargs):
        if 'key' in kwargs and kwargs['key'] is not None and len(kwargs['key'])>0:
            self.key=kwargs['key']
            self.key=self.key.encode("utf-8")
            base64_bytes = base64.b64encode(self.key)
            base64_string = base64_bytes.decode("utf-8")
            self.key=base64_bytes[:32]
            print(5* " key ")
            print(self.key)
            print(5* " key ")
            print(self.key)

        else:
            self.key = Fernet.generate_key()

    def encrypt(self,plain,*args, **kwargs):
        print(5* "__encrypt__key")
        print(self.key)
        print(5* "__encrypt__key")
        self.fernet = Fernet(self.key)
        encMessage = self.fernet.encrypt(plain.encode())
       
        return encMessage


    def decrypt(self,cypher,*args, **kwargs):
        encoding = 'utf-8'
        cypher=bytearray(cypher,encoding)
        cypher=bytes(cypher)
        self.key=bytearray(self.key,encoding)
        self.key=bytes(self.key)
        self.fernet = Fernet(self.key)
       
        decMessage = self.fernet.decrypt(cypher)
        
        return decMessage