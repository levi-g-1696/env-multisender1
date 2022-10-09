
import os.path, os
from ftplib import FTP, error_perm
from shutil import copy2
import csv
from collections import namedtuple
from  lib2 import confreader,copyFilesToArc,Remove1File,RemoveFilesFrom, removeOld,copyFilesFromList
import logging
import time, ftplib, glob
import pysftp as sftp
import globalConfig
import paramiko

# functions exported to main2: sendFolderFiles,CreateArcFolders,CopyAllFolders,NewPrepareTempFolders
#  sendFolderFiles
#     uses: Remove1File from lib2
#
#
#

import subprocess





def sendFolderFilesV7_33(session):# not good: tha files mus disapeer from upfolder, becouse every destinationn is a different channel
    protocol= str(session.protocol)
    protocol= protocol.lower()
    isSFTP = protocol.__contains__("sftp")
    isFtp = protocol.__contains__("ftp") and not (protocol.__contains__("sftp"))
    isSmb = protocol.__contains__("smb") or protocol.__contains__("shar")

    fileList = session.fileList   # must be full path for every file
   # upFolderPath = upfolder[i]
    #     print("prepare list for ftp, path :", tempFolderPath)
    numsent = 0
    for fileLocalpath in fileList:



        if os.path.isfile(fileLocalpath):
            try:
                if (isFtp) : push_file_FTP(session.ip,session.port,session.user, session.psw,fileLocalpath)
                elif (isSFTP ) : push_file_SFTP(session.ip,session.port,session.user, session.psw,fileLocalpath)
                elif (isSmb): print ("smb protocol is not impemented")
                numsent = numsent + 1
                 # print("placefile FTP  ", localpath)
                time.sleep(0.03)
                print("SYSTEM IS REMOVING" + fileLocalpath)
                Remove1File(fileLocalpath)
            except ftplib.all_errors as e:
                print("  ===> F T P exception on sending " , fileLocalpath, " user ", session.user, " to ", session.ip)
            except sftp.exceptions.ConnectionException  as es:
                raise es
        else:
            print("sendFolderFiles(session), 208.1,source content error")




    return numsent

#=========================================================================
def sendFolderFiles(session):
    protocol= str(session.protocol)
    protocol= protocol.lower()
    isSFTP = protocol.__contains__("sftp")
    isFtp = protocol.__contains__("ftp") and not (protocol.__contains__("sftp"))
    isSmb = protocol.__contains__("smb") or protocol.__contains__("shar")
    tempFolderPath = session.sourcefolder   # may be a mistake in name
   # upFolderPath = upfolder[i]
    #     print("prepare list for ftp, path :", tempFolderPath)
    numsent = 0
    for name in os.listdir(tempFolderPath):

        fileLocalpath = os.path.join(tempFolderPath, name)

        if os.path.isfile(fileLocalpath):
            try:
                if (isFtp) : push_file_FTP(session.ip,session.port,session.user, session.psw,fileLocalpath)
                elif (isSFTP ) : push_file_SFTP(session.ip,session.port,session.user, session.psw,fileLocalpath)
                elif (isSmb): print ("smb protocol is not impemented")
                numsent = numsent + 1
                 # print("placefile FTP  ", localpath)
                time.sleep(0.03)

                Remove1File(fileLocalpath)
            except ftplib.all_errors as e:
                print("  ===> F T P exception on sending " , fileLocalpath, " user ", session.user, " to ", session.ip)
            except sftp.exceptions.ConnectionException  as es:
                raise es
        else:
            print("main, 208.1,source content error")




    return numsent
#=======================================================================
def sendFolderFilesOldVer(session):
    protocol= str(session.protocol)
    protocol= protocol.lower()
    isSFTP = protocol.__contains__("sftp")
    isFtp = protocol.__contains__("ftp") and not (protocol.__contains__("sftp"))
    isSmb = protocol.__contains__("smb") or protocol.__contains__("shar")
    if (isFtp):
        ftp = FTP()
        ftp.connect(session.ip, int(session.port))
        ftp.login(session.user, session.psw)

        tempFolderPath = session.sourcefolder
       # upFolderPath = upfolder[i]
        #     print("prepare list for ftp, path :", tempFolderPath)
        numsent = 0
        for name in os.listdir(tempFolderPath):

            fileLocalpath = os.path.join(tempFolderPath, name)

            if os.path.isfile(fileLocalpath):
                try:
                    ftp.storbinary('STOR ' + name, open(fileLocalpath, 'rb'))
                    numsent = numsent + 1
                     # print("placefile FTP  ", localpath)
                    time.sleep(0.03)

                    Remove1File(fileLocalpath)
                except ftplib.all_errors as e:
                    print("  ===> F T P exception on sending " , fileLocalpath, " user ", session.user, " to ", session.ip)
            else:
                print("main, 208.1,source content error")
        ftp.quit()
    elif (isSFTP) : return
    elif (isSmb): return
    else : print( "  ===> Protocol type error : " + protocol + " user:"+ session.user)


    return numsent
#+++++++++++++++++++++==============================================

def push_file_FTP(ip,port,user, psw,filePath):
    ftp = FTP()
    ftp.connect(ip, int(port))
    ftp.login(user, psw)

    fileNameStrArr=str(filePath).split("\\")
    lastIndx= len(fileNameStrArr)-1
    fileName= fileNameStrArr[lastIndx]

    ftp.storbinary('STOR ' + fileName, open(filePath, 'rb'))
    ftp.close()
#=============     push_file_SFTP      =================================================


def push_file_SFTP(ip,port,user, psw,file):
    # ip user psw file - strings
   # file="C:\\Users\\wn10\\PycharmProjects\\multisender1.0\\initConfig.json"
    # port is string
    cnopts = sftp.CnOpts()
    cnopts.hostkeys = None
    s = sftp.Connection(host=ip, username= user, password=psw,
                        port = int(port),cnopts=cnopts)
  #  local_path ="C:\\Users\\wn10\\Desktop\\EnviroDoc\\LINKs\\mrc.txt"
#    remote_path = "REMOTE FILE PATH"

#   s.put(local_path, remote_path)
    s.put(file)
    s.close()

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#################################################################
def new_directory(directory):
  # Before creating a new directory, check to see if it already exists

  if os.path.isdir(directory) == False:
    os.makedirs(directory)
#################################################################

#=========================================
def CreateArcFolders(config,arcroot):
    arcfolder=[]
    users= config.users
    destinationHOST= config.hosts
    port= config.ports
    upfolder= config.sourcefolders
    for i in range(len(upfolder)):

        arcfolderStr= arcroot+"\\Arc"+  "-" + users[i]+"-"+destinationHOST[i]+"-"+port[i]
        new_directory(arcfolderStr)
        arcfolder.append(arcfolderStr)
     #   source = upfolder[i]
    #    dest = tempfolder[i]
  #      copyFilesToArc(source, dest) #we do an arc for every user-destination
    return arcfolder

#############################################

#=========================================
def CopyAllFolders(sourceArr,destArr):

    for i in range(len(sourceArr)):
      copyFilesToArc(sourceArr[i], destArr[i]) #we do an arc for every user-destination
    return


#=========================================
def RemoveFromUpfolder(upfolderDict):
    for key,val in upfolderDict.items():
       fileList= upfolderDict[key]
       for localpath in fileList:
         try:
            with open(localpath, encoding='utf-8') as f:
                xxxx = 1  ## no op to close localpath
            if os.path.isfile(localpath):
                open
                os.remove(localpath)

            else:
                print("RemoveFromUpfolder: source content error")
         except PermissionError as es:
            print("RemoveFromUpfolder : Pemission error")
    return


#===================================

#====================================


def NewPrepareTempFolders(config,temproot):
    tempfolder = []
    print ("making upfolder dictionary")
    upfolder = config.sourcefolders
    upFolderDict=MakeUpfolderDictionary(upfolder)

    for i in range(len(upfolder)):
        tempfolderStr= temproot+"\\Tmp"+  "-" + config.users[i]+"-"+config.hosts[i]+"-"+ config.ports[i]
        new_directory(tempfolderStr) #if doesnot exist
        tempfolder.append(tempfolderStr) #??? do we need it?
        print("copying to tempfolder ",tempfolderStr)
        key= config.sourcefolders[i]  #key="c:\z\zz\zzz"
        fileList = upFolderDict[key] #["1.txt,111.txt]
        copyFilesFromList(fileList, tempfolderStr) ###########copy all the files to folder
    RemoveFromUpfolder(upFolderDict) # remove only files registered in dictionary
    return tempfolder
#=========================================
#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
def MakeUpfolderDictionary(upfolder):

    upFolderDict = {}
    emptyArr=[]
    for i in range (len(upfolder)):
        upFolderDict[upfolder[i]]=emptyArr  # {"c:\z\zz\zzz",[]}
    for key,val in upFolderDict.items():
        upFolderDict[key] = GetFileList(key)  # {c:\z\zz\zzz",[1.txt,111.txt]}

    return  upFolderDict


#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
def GetFileList(path):
    fileList = []
    for name in os.listdir(path):
        localpath = os.path.join(path, name)

        if os.path.isfile(localpath):
            fileList.append(localpath)
        else:
            print("source content error")
    return fileList
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
def RemoveEmptyFolders(path_abs):
    root = path_abs
    folders = list(os.walk(root))[1:]

    for folder in folders:
        # folder example: ('FOLDER/3', [], ['file'])
        if not folder[2]:
            print (">  removing empty temporary folder : ",folder[0] )
            os.rmdir(folder[0])
            time.sleep(1)
