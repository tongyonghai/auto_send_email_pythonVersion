#!/usr/bin/python3
 
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.header import Header
import email
from email.mime.base import MIMEBase
import os
import re
import base64

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

class ecn_no_deliver_and_controlled_drawing_bill:
   def mainfun(self,sdict):
    smtp_server = 'smtp.qiye.163.com' 
    sender = sdict['sender']
    drawing_quantity=sdict['drawing_quantity']
    receivers = sdict['receivers'] # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    tel=sdict['tel']
    cc=sdict['cc']
    targedir=sdict['targetpath']
    subject =sdict['subject']
    password =base64.b64decode(sdict['password'])
    # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
    msgRoot = MIMEMultipart('guanlian')
    msgRoot['From'] = ';'.join(sender)  # 发送者
    msgRoot['To'] =  ';' .join(receivers)         # 接收者 
    msgRoot['cc']=';'.join(cc)
    msgRoot['Date']=email.utils.formatdate()    
    msgRoot['Subject'] = Header(subject, 'utf-8')
    index1=sender.find('<',0, -1)+1
    index2=sender.find('>',0, -1)
    mail_host = sender[index1:index2]    

    #targedir=r'D:\exctract_pdf_prj'
    file_dir_list = os.listdir(targedir) #列出文件夹下所有的目录与文件
    global filename, filepath,extname

    pattern='(ECN-未出货机器)'
    for i in range(0,len(file_dir_list)):
        path=os.path.join(targedir,file_dir_list[i])
        if os.path.isfile(path):
            r=re.findall(pattern,file_dir_list[i],0)
            if len(r):
                filename=file_dir_list[i]
                filepath=path            
                index= file_dir_list[i].find('-',0,-1)
                extname=file_dir_list[i][index+1:]
                break
    if len(filename)<=0:
        print('ECN-未出货机器文件不存在，请添加')
        sys.exit(0)

    msgRoot.attach(assembly_attach(filepath))

    pattern='(受控图纸清单及明细).*'
    for i in range(0,len(file_dir_list)):
        path=os.path.join(targedir,file_dir_list[i])
        if os.path.isfile(path):
            r=re.findall(pattern,file_dir_list[i],0)
            if len(r):
                filename=file_dir_list[i]
                filepath=path            
                index= file_dir_list[i].find('-',0,-1)
                extname=file_dir_list[i][index+1:]
                break
    if len(filename)<=0:
        print('受控图纸清单及明细文件不存在，请添加')
        sys.exit(0)

    msgRoot.attach(assembly_attach(filepath))


    msgAlternative = MIMEMultipart('alternative')
    msgRoot.attach(msgAlternative)
    mail_msg = """
    <p>Dear All</p>
    <p> 最新已受控图纸"""
    mail_msg +=str(drawing_quantity)

    mail_msg +="""份</p>
    <p>工程变更-未出货机器信息，清单详见附件!</p>
    <hr style="height:5px;background-color:#000;" />
    <b>
    <p  >"""

    mail_msg+=sender[0:sender.find("<",0,-1)]
    mail_msg+="""</p>
    </b>
    <p>工程技术部/管理部</p>
    <p><img src="cid:image1"></p>
    <p>长园和鹰智能科技（苏州）有限公司</p>
    <p>Mobile："""

    mail_msg+=tel
    mail_msg+="""</p>
    <p>Address：苏州太湖国家旅游度假区孙武路2993号的文创中心2号楼9层</p>
    <b>
    <p>“重要提示：电子邮件属于个人行为，凡与本公司进行任何商业交易均需经过本公司盖章确认，才能对本公司生效。”</p>
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

