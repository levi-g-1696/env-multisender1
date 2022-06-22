

import os.path, os
from ftplib import FTP, error_perm
from shutil import copy2
import csv
from  lib2 import confreader,copyFilesToArc,Remove1File,RemoveFilesFrom, removeOld
import logging
import time, ftplib, glob
from libFileTransfer import sendTempFolderFiles1
import subprocess

def sendTempFolderFiles(tempfolder,i):


    ftp.connect(destinationHOST[i], int(port[i]))
    ftp.login(users[i], passw[i])

    tempFolderPath = tempfolder[i]
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
                print("  ===> F T P exception on sending " , fileLocalpath, " user ", users[i], " to ", destinationHOST[i])
        else:
            print("main, 208,source content error")
    ftp.quit()
    return numsent

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def AddToExceptIParr(n,value):
    l= list( ftpExceptIParr)

    num = n -l.count(value)
    for i in range(1,num):
        ftpExceptIParr.append(value)
    return
#################################################################
def new_directory(directory):
  # Before creating a new directory, check to see if it already exists

  if os.path.isdir(directory) == False:
    os.makedirs(directory)

#############################################################3
def PrepareTempFolders(upfolder):
    tempfolder=[]
    for i in range(len(upfolder)):

        tempfolderStr= temproot+"\\Tmp"+  "-" + users[i]+"-"+destinationHOST[i]+"-"+port[i]
        new_directory(tempfolderStr)
        tempfolder.append(tempfolderStr)
        source = upfolder[i]
        dest = tempfolder[i]
        copyFilesToArc(source, dest)
    return tempfolder
#=========================================
def CreateArcFolders(upfolder):
    arcfolder=[]
    for i in range(len(upfolder)):

        arcfolderStr= arcroot+"\\Arc"+  "-" + users[i]+"-"+destinationHOST[i]+"-"+port[i]
        new_directory(arcfolderStr)
        arcfolder.append(arcfolderStr)
     #   source = upfolder[i]
    #    dest = tempfolder[i]
  #      copyFilesToArc(source, dest) #we do an arc for every user-destination
    return arcfolder
#=========================================
def CopyAllFolders(sourceArr,destArr):

    for i in range(len(sourceArr)):
      copyFilesToArc(sourceArr[i], destArr[i]) #we do an arc for every user-destination
    return
#=========================================

#====================================


if __name__ == "__main__":
    ## stoping option  ##
    st = "c:\\ftpTransfer\\stop.conf"

    os.chdir("C:\\Users\\wn10\\PycharmProjects\\multisender1.0")
    configFile = ".\\transferConfig22.csv"
    log = ".\\Log\\transferLog.csv"
    temproot = ".\\Temp"
    arcroot=  ".\\Arc"
    logoldpath = ".\\LogOld\\"
    ftpExceptIParr = []
    ftpExceptEscapecount = 30
    st = "c:\\ftpTransfer\\stop.conf"
    continueFlag = True

#--------------------------------
    try:
        os.remove(st)
    except FileNotFoundError as e:
        print("Cannot find stop.conf")

    f1 = open(st, 'w')
    f1.write('stopFlag=0\n')  # python will convert \n to os.linesep
    f1.close()  # you can omit in most cases as the destructor will call it
    continueFlag = True
    ######################
    f1 = open(log, "r")
    logfileid = f1.fileno
    f1.close
    ###################
    print()
    print("    ftp transfer is started\r\n")
    j = 0
    m = 0


#-----------

#=====================================

    isEnable,isLastDest, users, passw, upfolder,  destinationHOST, port = confreader(configFile)

# ===== prepare temporary folders from upfolders  =====

    tempfolder = PrepareTempFolders(upfolder)   #make and fill tempfoders()
    arcfolder= CreateArcFolders(upfolder) # make arcfolder if not exist
    CopyAllFolders(upfolder, arcfolder) #we do an arc for every user-destination

    while (continueFlag):

        ftp = FTP()

        logging.basicConfig(filename=log, level=logging.INFO, format='%(asctime)s %(message)s',
                            datefmt='%d/%m/%Y %H:%M:%S')


#===========================================================


        for i in range(len(users)):
            try:
                ftpExceptIP = users[i] + "-" + destinationHOST[i] + "-" + port[i]
                if ( ftpExceptIP  in ftpExceptIParr) :
                    ## host was not reachable not send it
                    ftpExceptIParr.remove(ftpExceptIP)
                    time.sleep(0.25)
                else:
                    #if host was ok - send
                #    sendtempfoderFiles()
                    numsent=  sendTempFolderFiles(tempfolder, i)
                   # numsent= sendTempFolderFiles1(destinationHOST[i],port[i],tempfolder,users[i],passw[i])
                    logging.info("," + destinationHOST[i] + "," + users[i] + "," + upfolder[i])
              #      print( "  ", numsent , " files were sent to " ,destinationHOST[i], users[i])
                    print("  ", numsent, " files were sent to ", destinationHOST[i], users[i])


            except ftplib.all_errors as e:
                print(" \n> > > >   F T P exception  - ", destinationHOST[i], users[i],str(e),"\n")

                time.sleep(0.1)

                AddToExceptIParr( 10, ftpExceptIP) #10 ip numbers to array if destination is not reachable

              #  ftpExceptEscapecount = 10
                logging.info("," + destinationHOST[i] + "," + users[i] + "," + upfolder[i] + "," + "Error " + str(e))

        time.sleep(0.15)
        isEnable,isLastDest, users, passw, upfolder,  destinationHOST, port = confreader(configFile)
        CopyAllFolders(upfolder, arcfolder)
        CopyAllFolders(upfolder,tempfolder)