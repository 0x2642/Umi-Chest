#-*- coding: UTF-8 -*-
import socket,os
import const,common,upload,cryptofactory


class Deal:
    CONST=const
    CONST.BUFFSIZE=1024

    comm = common.Common()

    def __init__(self):
        obj = socket.socket()

        obj.connect((self.comm.getClientConf("server","host"),int(self.comm.getClientConf("server","port"))))

        ret_bytes = obj.recv(self.CONST.BUFFSIZE)
        ret_str = self.comm.tanslate(str(ret_bytes))
        print(ret_str)

        while True:
            inp = raw_input(self.comm.tanslate("你好请问您有什么问题？ \n >>>") )
            if inp == "q":
                inp = cryptofactory.CryptoFactory().encrypto(inp,self.comm.getClientConf("transmission","crypto_key"))
                data=self.comm.createPacket(inp,0)
                obj.sendall(bytes(data))
                break
            elif inp == "upload":
                upload.Upload(obj)
            else:
                inp = cryptofactory.CryptoFactory().encrypto(inp,self.comm.getClientConf("transmission","crypto_key"))
                data=self.comm.createPacket(inp,99999,"text")
                obj.sendall(bytes(data))
                ret_bytes = obj.recv(self.CONST.BUFFSIZE)
                ret_str = self.comm.tanslate(str(ret_bytes))
                print(ret_str+"112233")



