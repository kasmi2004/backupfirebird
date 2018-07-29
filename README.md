# backupfirebird.py
# Autor: Antonio Carlos Nunes Júnior - Avalue Sistemas LTDA.

Realiza Backup de Banco de Dados Firebird de um servidor Linux na Amazon para o S3 da amazon aws utilizando Python

Este arquivo realiza backup em pastas e subpastas ondem contém arquivos com extensão .fdb, fiz para fazer backups dos meus banco
de dados em Firebird, é compatível com Firebird 2 e 3, o backup é enviado para o storage S3 da amazon aws, foi utilizado.

Pacotes utilizados.

boto3
sendgrid
fdb

pip install boto3
pip install fdb
pip install sendgrid
