#!/usr/bin/python3
# -*- coding: utf-8 -*- 
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.header import Header
import email
from email.mime.base import MIMEBase
import os
import zipfile
import re
import base64

def zip_ya(startdir,file_news):   
    file_news = startdir +'.zip' # 压缩后文件夹的名字
    z = zipfile.ZipFile(file_news,'w',zipfile.ZIP_DEFLATED) #参数一：文件夹名
    for dirpath, dirnames, filenames in os.walk(startdir):
        fpath = dirpath.replace(startdir,'') #这一句很重要，不replace的话，就从根目录开始复制
        fpath = fpath and fpath + os.sep or ''#这句话理解我也点郁闷，实现当前文件夹以及包含的所有文件的压缩
        for filename in filenames:
            z.write(os.path.join(dirpath, filename),fpath+filename)
            #print ('压缩成功')
    z.close()
       
def assembly_attach(file_path):
    contype = 'application/octet-stream'
    maintype, subtype = contype.split('/', 1)    
    data = open(file_path, 'rb')
    file_msg = MIMEBase(maintype, subtype)
    file_msg.set_payload(data.read())
    data.close()
    email.encoders.encode_base64(file_msg)
    basename = os.path.basename(file_path.split('/')[-1])
    file_msg.add_header('Content-Disposition', 'attachment', filename=basename)
    return file_msg
class contract_estimate:
   def mainfun(self,sdict):
        smtp_server = 'smtp.qiye.163.com'
        sender = sdict['sender']
        #drawing_quantity=sdict['drawing_quantity']
        receivers = sdict['receivers'] # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
        tel=sdict['tel']
        cc=sdict['cc']
        targedir=sdict['targetpath']
        subject =sdict['subject']
        ps=sdict['password']
        password =str(base64.b64decode(ps),'utf-8')
        
        msgRoot = MIMEMultipart('guanlian')
        msgRoot['From'] = ';'.join(sender)  # 发送者
        msgRoot['To'] =  ';' .join(receivers)         # 接收者 
        #msgRoot['cc']=';'.join(cc)
        msgRoot['Date']=email.utils.formatdate()       
        msgRoot['Subject'] = Header(subject, 'utf-8')
        index1=sender.find('<',0, -1)+1
        index2=sender.find('>',0, -1)
        mail_host = sender[index1:index2]
        #targedir=r'D:\exctract_pdf_prj'
        file_dir_list = os.listdir(targedir) #列出文件夹下所有的目录与文件
        pattern='^(合同评审表).*'
        global sendfoldsname,dirpath,foldsname,extname
        for i in range(0,len(file_dir_list)):
            path=os.path.join(targedir,file_dir_list[i])
            if os.path.isdir(path):
                r=re.findall(pattern,file_dir_list[i],0)
                if len(r):
                    foldsname=file_dir_list[i]
                    dirpath=path
                    sendfoldsname=path+'.zip'
                    index= file_dir_list[i].find('-',0,-1)
                    extname=file_dir_list[i][index+1:]
                    break
        if len(foldsname)<=0:
            print('合同评单文件夹不存在，请添加')
            sys.exit(0)
        #dirpath=r'D:\exctract_pdf_prj\合同评审表-WK41'
        filelist=os.listdir(dirpath) #提取文件列表
        result="<table  border=\"1\"> <th bgcolor=\"#009900\">合同号</th>"
        for i in range(0,len(filelist)):
            result+="<tr><td>"+filelist[i][:-4]+"</td> </tr>"
        result+="</table>"

        zip_ya(dirpath,'') #压缩文件夹为zip文件
        msgRoot.attach(assembly_attach(sendfoldsname))

        msgAlternative = MIMEMultipart('alternative')
        msgRoot.attach(msgAlternative)
        mail_msg = """
        <p>Dear All</p>
        <p> 附件为 合同评审表-"""
        mail_msg+=extname

        mail_msg+= """，清单如下：</p>"""+result

        mail_msg+="""<hr style=\"height:2px;width=50px;background-color:#000;\" />
        <b>
        <p >""";
        mail_msg+=sender[0:sender.find("<",0,-1)]

        mail_msg+="""
        </p>
        </b>
        <p>工程技术部/管理部</p>
        <p><img src="cid:image1"></p>
        <p>长园和鹰智能科技（苏州）有限公司</p>
        <p>Mobile："""
        mail_msg+=tel

        mail_msg+="""</p>
        <p>Address：苏州太湖国家旅游度假区孙武路2993号的文创中心2号楼9层</p>
        <b>
        <p>\"重要提示：电子邮件属于个人行为，凡与本公司进行任何商业交易均需经过本公司盖章确认，才能对本公司生效。\"</p>
        </b>
        """
        msgAlternative.attach(MIMEText(mail_msg, 'html', 'utf-8'))

        # 指定图片为当前目录
        fp = open('companylogo.jpg', 'rb')
        msgImage = MIMEImage(fp.read())
        fp.close()
 
        # 定义图片 ID，在 HTML 文本中引用
        msgImage.add_header('Content-ID', '<image1>')
        msgRoot.attach(msgImage)
        try:
            smtpObj = smtplib.SMTP(host=smtp_server,port=25)    
            smtpObj.login(mail_host,password)
            smtpObj.sendmail(sender, receivers, msgRoot.as_string())
            print ("邮件发送成功")
        except smtplib.SMTPException as ex:
            print ('1:'+ex.errno)
        except smtplib.SMTPAuthenticationError as ex2:
            print('2:'+ex2.errno)