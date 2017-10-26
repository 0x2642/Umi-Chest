#-*- coding: UTF-8 -*-
import socketserver,cryptofactory,common,constTable,const,uploadDeal
class UmiChestServer(socketserver.BaseRequestHandler):
    comm=common.Common()
    CONST=const
    CONST.METHOD=constTable.constTable().METHOD
    def handle(self):
        conn = self.request
        conn.sendall(bytes("你好，我是机器人"))
        up=uploadDeal.UploadDeal()
        cf=cryptofactory.CryptoFactory()
        while True:
            flag=False
            totol_data=""
            ret_bytes = str(conn.recv(1024))
            totol_data+=ret_bytes
            if ret_bytes[-1:] != "\0":
                while True:
                    ret_bytes = str(conn.recv(1024))
                    totol_data+=ret_bytes
                    if ret_bytes[-1:] == "\0" or not ret_bytes:
                        break

            ret_str_packet = str(totol_data)
            ret_str_packet = ret_str_packet.split("\0")
            # 去除\0的空元素
            ret_str_packet=ret_str_packet[:-1]

            for ret_str in ret_str_packet:

                ret_str_list=ret_str[:-1].split("\n")
                # print(ret_str_list)
                ret_dict={}
                for r in ret_str_list:
                    r=r.split(":")
                    # print(r)
                    if len(r)>1:
                        ret_dict[r[0]]=r[1]

                # print(ret_dict['md5'])
                ret_msg=""
                data=cf.decrypto(ret_dict['data'],self.comm.getClientConf("transmission","crypto_key"))
                if data == "q":
                    flag=True
                    break
                elif ret_dict['method'].upper() == self.CONST.METHOD["upload"]:
                    ret_msg = up.savePackage(data,ret_dict)
                    # print(ret_msg)
                    if up.isFinish(ret_dict,len(data)):
                        up.syntheticFile(ret_dict)
                else:
                    ret_msg = data+"11ss22"
                conn.sendall(bytes(ret_msg))

            if flag:
                break

