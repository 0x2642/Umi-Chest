# -*- coding: utf-8 -*-

import zipfile,os,time,random,hashlib,json,ConfigParser,const,sys,uuid

class Common:
    CONST=const
    CONST.RUNTIME_PATH=os.path.dirname(os.path.realpath(__file__))+"/../runtime"
    CONST.CONF_PATH=os.path.dirname(os.path.realpath(__file__))+"/../config"

    def __init__(self):
        pass

    def dp(self,obj):
        print(obj)
        sys.exit(-1)

    def tanslate(self,str,form_code="utf-8",to_code="cp936"):
        return str.decode(form_code).encode(to_code)

    def dict2json(self,dict):
        return json.dumps(dict)

    def json2dict(self,json_str):
        return json.loads(json_str)

    def readBinFile(self,fs,length):
            return fs.read(length)

    def writeBinFile(self,path,text,mode="wb"):
        pass

    def readFile(self,path,mode):
        file = open(path, mode)
        try:
           text = file.read()
        finally:
            file.close()
        return text

    def writeFile(self,path,text,mode):
        file = open(path, mode)
        try:
            file.write(text)
        finally:
            file.close()

    def baleZip(self,form_file_path,to_file_path):
        to_file_path+=".zip"
        z = zipfile.ZipFile(to_file_path, 'w', zipfile.ZIP_DEFLATED)
        startdir = form_file_path
        child_list=[]
        self.baleFolder(startdir,child_list)

        for filename in child_list:
            pre_len = len(os.path.dirname(filename))
            arcname = filename[pre_len:].strip(os.path.sep)   #相对路径
            z.write(filename, arcname)
        z.close()
        return to_file_path

    def baleFolder(self,dir_path,child_list):
        parents = os.listdir(dir_path)
        for parent in parents:
            child = os.path.join(dir_path,parent)
            if os.path.isdir(child):
                if os.stat(child).st_size<=0:
                    child_list.append(child)
                else:
                    child_list =  self.baleFolder(child,child_list)
            else:
                child_list.append(child)
        return child_list

    def getRuntimeDir(self):

        if not os.path.exists(self.CONST.RUNTIME_PATH):
            os.makedirs(self.CONST.RUNTIME_PATH)

        return self.CONST.RUNTIME_PATH+"/"+self.md5(str(time.time())+str(random.random()))

    def md5(self,str):
        m = hashlib.md5()
        m.update(str)
        return m.hexdigest()

    def getConf(self,conf_path,section,option):
        cf = ConfigParser.ConfigParser()
        cf.read(conf_path)
        return cf.get(section,option)

    def getClientConf(self,section,option):
        return self.getConf(self.CONST.CONF_PATH,section,option)

    def createPacket(self,data,package_num,method="",uuid=""):
        head={
                "method":method,
                "package_num":package_num,
                "size":len(data),
                "md5":self.md5(data),
                "data":data,
                "uuid":uuid
             }
        packet=""
        for key, value in head.items():
            if(str(value)!=""):
                packet+=str(key)+":"+str(value)+"\n"
        return packet+"\0"