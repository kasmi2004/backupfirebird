# -*- coding: utf-8 -*-
# Fazer o backup do banco de dados firebird para o storage s3 da amazon aws
# O mesmo será  backupeado antes no serviço firebird e depois zipado e upado para o S3 do seu servidor
# Autor : Antonio Carlos Nunes Júnior - Avalue Sistemas LTDA
import boto3
import os
import zipfile
import calendar
from datetime import date
import sendgrid 
from sendgrid.helpers.mail import *
from fdb import services

aws_access_key_id='**'
aws_secret_access_key='**'
path='/your/path/'
output = []

s3 = boto3.resource('s3',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
)

def Sucess(file):
    nomearquivo=os.path.basename(os.path.dirname(file))
    sg = sendgrid.SendGridAPIClient(apikey='**')
    from_email = Email("youremail@youemail.com")
    to_email = Email("toemail@toemail.com")
    subject = "Backup de --> %s" % nomearquivo
    content = Content("text/plain", "Backup Firebird - log do arquivo %s feito com sucesso!" % nomearquivo + '\n'.join(output))
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())

def FetchLine(line):
    output.append(line)

def RemoveBackup(file):
    pathRemove=path + os.path.dirname(file)
    RemoveFbk=pathRemove + '/*.fbk'
    RemoveLog=pathRemove + '/*.log'
    RemoveZip=pathRemove + '/' + os.path.basename(file)
    os.remove(RemoveFbk)
    os.remove(RemoveLog)
    os.remove(RemoveZip)
    Sucess(file)

def ZipFirebird(file):
    weekday=calendar.day_name[date.today().weekday()]
    path=os.path.dirname(file)
    filezip = zipfile.ZipFile(path + '/%s-seuarquivo.zip' % weekday, 'w') 
    filezip.write(path + '/seuarquivo.fbk')
    filezip.write(path + '/seuarquivo.log')
    filezip.close
    return filezip.filename

def BackupFirebird(file):
    path=os.path.dirname(file)
    con = services.connect(host='localhost', user='sysdba', password='yourpassword')
    file_fdb=file
    file_fbk=path + '/seuarquivo.fbk'
    con.backup(file_fdb, file_fbk, collect_garbage=False, callback=FetchLine)
    with open(path + '/seuarquivo.log', 'w') as f:
        for line in output:
            f.write(line+'\n')
        f.close

    return ZipFirebird(file)

def UploadS3(path,file):
    file = BackupFirebird(file)
    data = open(file, 'rb')
    file = path + "/" + os.path.basename(file)
    s3.Bucket('yourbucket').put_object(Key='your-folder/' + file, Body=data)
    RemoveBackup(file)

for root, dirs, files in os.walk(path):
    for filename in files:
        if filename.endswith('.fdb'):
            UploadS3(os.path.basename(root), os.path.join(root, filename))
            output = []
            
print "Finalizado com sucesso os backups!"