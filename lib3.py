
import os.path, os
from ftplib import FTP, error_perm
from shutil import copy2
import csv
from collections import namedtuple
from  lib2 import confreader,copyFilesToArc,Remove1File,RemoveFilesFrom, removeOld,copyFilesFromList
import logging
import time, ftplib, glob
# functions exported to main2: sendFolderFiles,CreateArcFolders,CopyAllFolders,NewPrepareTempFolders
#  sendFolderFiles
#     uses: Remove1File from lib2
#
#
#

import subprocess



def sendFolderFiles(session):
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
    return numsent

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
#====================================

def NewPrepareTempFolders(config,temproot):
    tempfolder = []
    print ("making upfolder dictionary")
    upfolder = config.sourcefolders
    upFolderDict=MakeUpfolderDictionary(upfolder)

    for i in range(len(upfolder)):
        tempfolderStr= temproot+"\\Tmp"+  "-" + config.users[i]+"-"+config.hosts[i]+"-"+ config.ports[i]
        new_directory(tempfolderStr)
        tempfolder.append(tempfolderStr) #??? do we need it?
        print("copying to tempfolder ",tempfolderStr)
        key= config.sourcefolders[i]
        fileList = upFolderDict[key]
        copyFilesFromList(fileList, tempfolderStr) ###########must check
    RemoveFromUpfolder(upFolderDict)
    return tempfolder
#=========================================
#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
def MakeUpfolderDictionary(upfolder):

    upFolderDict = {}
    emptyArr=[]
    for i in range (len(upfolder)):
        upFolderDict[upfolder[i]]=emptyArr
    for key,val in upFolderDict.items():
        upFolderDict[key] = GetFileList(key)

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