# -*- coding: utf-8 -*-
import base64

class CryptoBase64:
    def __init__(self):
        pass

    def encrypto(self,text,key):
        return base64.b64encode(text)

    def decrypto(self,text,key):
        return base64.b64decode(text)