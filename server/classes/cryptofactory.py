# -*- coding: utf-8 -*-
import common,crypto,sys,os

class CryptoFactory:
    comm = common.Common()
    cryptoType="None"
    cryptoMod=""
    def __init__(self):
        parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"/crypto"
        sys.path.insert(0,parentdir)
        self.cryptoType=self.comm.getClientConf("transmission","crypto")
        if self.cryptoType=="" or self.cryptoType.lower()=="none":
            self.cryptoMod = crypto.CryptoBase64.CryptoBase64()
        elif self.cryptoType.lower() =="aes":
            self.cryptoMod = crypto.AES.AES()
        elif self.cryptoType.lower() =="defalut":
            self.cryptoMod = crypto.DefCrypto.DefCrypto()

    def encrypto(self,text,key):
        return self.cryptoMod.encrypto(text,key)

    def decrypto(self,text,key):
        return self.cryptoMod.decrypto(text,key)