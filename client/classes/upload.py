# -*- coding: utf-8 -*-

import common,os,const,cryptofactory,sys,uuid

class Upload:
    comm = common.Common()
    CONST=const
    CONST.TRANSMISSION_UNIT=2048
    uid=uuid.uuid1()

    def __init__(self,socket_obj):
        self.run(socket_obj)

    def run(self,socket_obj):
        self.createNewUpload(socket_obj)

    def createNewUpload(self,socket_obj):
        dir_id=uuid.uuid1()
        flag=False
        while True:
            if flag:
                print(self.comm.tanslate("要上传的文件不存在！\n"))
            file_path=raw_input(self.comm.tanslate("请输入需要上传的文件路径"))

            if os.path.exists(file_path):
                break
            else:
                flag=True

        runtime_path=self.comm.getRuntimeDir()
        file_name=os.path.basename(file_path)
        file_type="file"
        if os.path.isdir(file_path):
            file_path = self.comm.baleZip(file_path,runtime_path)
            file_type = "dir"



        file_size= os.stat(file_path).st_size

        file_completed_size=0

        info_path=runtime_path+".cfg"

        file_info={"file_size":file_size,
                   "file_name":file_name,
                   "file_type":file_type,
                   "file_path":file_path,
                   "file_completed_size":file_completed_size}

        if not os.path.exists(info_path):
           self.setUploadInfo(info_path,file_info)

        file_info = self.getUploadInfo(info_path)
        fs = open(file_info['file_path'], 'rb')

        # 发送基础文件信息包
        self.sendUploadPackage(cryptofactory.CryptoFactory().encrypto(self.comm.dict2json(file_info),self.comm.getClientConf("transmission","crypto_key")),socket_obj,0,"UP")
        # self.comm.dp(total_package)
        # 必须要收包，否则有可能因为包太大导致在缓存区只读取该包，最后导致相差一个包
        self.recvPackage(socket_obj)

        package_num=1
        success_list=[]
        fail_list=[]

        resend_flag=False
        resend_count=0
        cf=cryptofactory.CryptoFactory()
        while True:
            with open(file_info['file_path'], 'rb') as f:
                for buff in f:
                    sl=[]
                    fl=[]
                    buff = cf.encrypto(buff,self.comm.getClientConf("transmission","crypto_key"))

                    if resend_flag:
                        if  len(fail_list) and package_num in fail_list:
                            self.sendUploadPackage(buff,socket_obj,package_num,"UP")
                            sl,fl=self.recvPackage(socket_obj)
                            fail_list.remove(package_num)
                    else:
                        self.sendUploadPackage(buff,socket_obj,package_num,"UP")
                        sl,fl=self.recvPackage(socket_obj)
                    package_num+=1
                    success_list+=sl
                    fail_list+=fl
                    # 成功修改cfg文件,失败加入重发队列
                    if len(sl)>0:
                        for sp in sl:
                            file_info['file_completed_size']+=int(sp['size'])
                            file_info = self.setUploadInfo(info_path,file_info)

                    # 成功修改cfg文件,失败加入重发队列


            if file_info['file_completed_size'] == file_size or resend_count>10:
                break
            else:
                resend_flag=True
                resend_count+=1


                    # self.comm.writeFile("./aaa.txt",str(len(buff))+","+str(read_file_size)+","+str(file_info['file_size'])+","+str(package_num)+"\n","a+")


        print(self.getUploadInfo(info_path))

    def sendUploadPackage(self,data,socket_obj,package_num,method=""):
        data=self.comm.createPacket(data,package_num,method,self.uid)
        socket_obj.sendall(bytes(data))


    def recvPackage(self,socket_obj):
        totol_data=""
        ret_bytes = socket_obj.recv(self.CONST.BUFFSIZE)
        ret_bytes = str(ret_bytes)
        totol_data+=ret_bytes
        if ret_bytes[-1:] != "\0":
            while True:
                ret_bytes = str(socket_obj.recv(self.CONST.BUFFSIZE))
                totol_data+=ret_bytes

                if ret_bytes[-1:] == "\0" or not ret_bytes:
                    break

        ret_str_packet = str(totol_data)

        ret_str_packet = ret_str_packet.split("\0")
        # 去除\0的空元素
        ret_str_packet=ret_str_packet[:-1]
        # 处理粘包
        success_list=[]
        fail_list=[]
        for ret_str in ret_str_packet:

            ret_str_list=ret_str[:-1].split("\n")
            # print(ret_str_list)
            ret_dict={}
            for r in ret_str_list:
                r=r.split(":")
                # print(r)
                if len(r)>1:
                    ret_dict[r[0]]=r[1]
            print(ret_dict)
            if ret_dict['status'] == "0" :
                success_list.append({"package_num":ret_dict['package_num'],"size":ret_dict['data'].split("|")[1]})
            else:
                fail_list.append(ret_dict['package_num'])

        return success_list,fail_list



    def getUploadInfo(self,info_path):

        file_info = self.comm.readFile(info_path,"rb")

        file_info = self.comm.json2dict(file_info)

        return file_info

    def setUploadInfo(self,info_path,file_info):

        self.comm.writeFile(info_path, self.comm.dict2json(file_info),"wb")
        return file_info
