# -*- coding: utf-8 -*-
import base64

class AES:
    def __init__(self):
        pass

    def encrypto(self,text):
        return base64.b64encode(text)

    def decrypto(self,text):
        return base64.b64decode(text)
