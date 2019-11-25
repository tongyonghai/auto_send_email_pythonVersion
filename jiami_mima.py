import base64
import threading
import os
if __name__== "__main__":
    s=input('邮箱密码=')
    
    s1=s.encode("utf-8")
    #print('mima:%s'%s1)
    bs = base64.b64encode(s1) # 将字符为unicode编码
    print('加密后的密码= %s'%str(bs,'utf-8'))
    bbs = str(base64.b64decode(bs), "utf-8")
    bbs1=base64.b64decode(bs).decode("utf-8");
    print('解码结果= %s'%bbs1) 
    os.system("pause")
   

