# -*- coding: utf-8 -*-
import base64

class DefCrypto:
    PASSWORD_TABLE="zaq12WSXcde34RFVbgt56YHNmju78IKlo90P+-=/pOLkiUJMnhyTGBvfrEDCxswQAZ"
    def __init__(self):
        pass

    def encrypto(self,text,key):
        text = base64.b64encode(text)
        tl=len(self.PASSWORD_TABLE)
        lpt=list(self.PASSWORD_TABLE)
        pw=[]
        for t in text:
            pw.append(lpt[(lpt.index(t)+int(key))%tl])
        return "".join(pw)

    def decrypto(self,text,key):
        tl=len(self.PASSWORD_TABLE)
        sw=[]
        lpt=list(self.PASSWORD_TABLE)
        for t in text:
            pos=lpt.index(t)
            for p in xrange(0,tl):
                if (p+int(key))%tl==pos:
                    sw.append(lpt[p])
        return base64.b64decode("".join(sw))
