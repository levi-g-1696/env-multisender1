# import pysftp
# import sys
#
# path = './THETARGETDIRECTORY/' + sys.argv[1]    #hard-coded
# localpath = sys.argv[1]
#
# host = "THEHOST.com"                    #hard-coded
# password = "THEPASSWORD"                #hard-coded
# username = "THEUSERNAME"                #hard-coded
#
# with pysftp.Connection(host, username=username, password=password) as sftp:
#     sftp.put(localpath, path)
#
# print ('Upload done.')
#

import pysftp as sftp
import paramiko


connection_info = {
    'server': "84.110.115.67",
    'user': "newtest",
    'passwd': "erm12345!",
    'port': 22
}
connection_info2 = {
    'server': "192.168.4.240",
    'user': "newtest",
    'passwd': "erm12345!",
    'port': 6022
}
cnopts = sftp.CnOpts()
cnopts.hostkeys = None

#with pysftp.Connection(host, username, password, cnopts=cnopts) as sftp:
def push_file_to_server():
    s = sftp.Connection(host=connection_info['server'], username=connection_info['user'], password=connection_info['passwd'],
                        port = connection_info['port'],cnopts=cnopts)
    local_path ="C:\\Users\\wn10\\Desktop\\EnviroDoc\\LINKs\\mrc.txt"
    remote_path = "REMOTE FILE PATH"

#   s.put(local_path, remote_path)
    s.put(local_path)
    s.close()


def push_file_SFTP(ip,port,user, psw,file):
    s = sftp.Connection(host=ip, username= user, password=psw,
                        port =port,cnopts=cnopts)
  #  local_path ="C:\\Users\\wn10\\Desktop\\EnviroDoc\\LINKs\\mrc.txt"
#    remote_path = "REMOTE FILE PATH"

#   s.put(local_path, remote_path)
    s.put(file)
    s.close()

def PushFileSFTP_paramiko(ip,port,user, psw,file):

    transport = paramiko.Transport((ip, port))
# Auth

    transport.connect(None,user,psw)
    sftp = paramiko.SFTPClient.from_transport(transport)
    sftp.put(file,"/test1225.txt")
    sftp.close()

#push_file_to_server()
paramiko.util.log_to_file("paramiko.log")
host=connection_info2['server']
username=connection_info2['user']
port = connection_info2['port']
password=connection_info2['passwd']
filePath="C:\\Users\\wn10\\Desktop\\EnviroDoc\\LINKs\\mrc.txt"
port=connection_info['port']
cnopts=cnopts
push_file_SFTP(host,port,username,password,filePath)
#PushFileSFTP_paramiko(host,6022,username,password,filePath)

