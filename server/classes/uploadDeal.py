# -*- coding: utf-8 -*-

import common,const,sys,constTable,os,shutil

class UploadDeal:
    comm=common.Common()
    CONST=const
    CONST.METHOD=constTable.constTable().METHOD
    def __init__(self):
        pass

    def savePackage(self,data,info):
        if(self.comm.md5(info['data'])!=info['md5']):
          return  self.comm.createRetStrPackage(info['package_num'],"MD5_VERIFICATION",len(data))
        runtime_path=self.comm.getRuntimeDir(self.CONST.METHOD['upload'],True,info['uuid'])

        self.comm.writeFile(runtime_path+"/"+info['package_num'],data,"wb+")
        return self.comm.createRetStrPackage(info['package_num'],"SUCCESS",len(data))

    def isFinish(self,info,length):
        runtime_path=self.comm.getRuntimeDir(self.CONST.METHOD['upload'],True,info['uuid'])
        desc_file=runtime_path+"/0"
        file_info={}
        flag=False
        if os.path.exists(desc_file):
            file_info = self.comm.json2dict(self.comm.readFile(desc_file,"r"))
            if file_info['file_completed_size']+length==file_info['file_size']:
                flag=True
            else:
                file_info['file_completed_size']=self.comm.getDirSize(runtime_path)-self.comm.getFileSize(desc_file)
                self.comm.writeFile(desc_file,self.comm.dict2json(file_info),"w+")

        return flag

    def syntheticFile(self,info):
        runtime_path=self.comm.getRuntimeDir(self.CONST.METHOD['upload'],True,info['uuid'])
        desc_file=runtime_path+"/0"
        file_list=[]
        for root, dirs, files in os.walk(runtime_path):
            for f in files:
                file_list.append(f)
        file_list=sorted(file_list)
        file_info = self.comm.json2dict(self.comm.readFile(desc_file,"r"))
        target_file=runtime_path+"/../"+info['uuid']+os.path.splitext(file_info['file_path'])[1]

        for f in file_list:
            file_path=runtime_path+"/"+f
            if file_path !=desc_file:
                self.comm.writeFile(target_file,self.comm.readFile(runtime_path+"/"+f,"rb"),"ab+")

        shutil.rmtree(runtime_path)