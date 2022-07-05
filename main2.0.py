

import os.path, os
from ftplib import FTP, error_perm
from shutil import copy2
import csv
from collections import namedtuple
from  lib2 import confreader,copyFilesToArc,Remove1File,RemoveFilesFrom, removeOld,copyFilesFromList
import logging
import time, ftplib, glob
from lib3 import sendFolderFiles,CreateArcFolders,CopyAllFolders,NewPrepareTempFolders
import subprocess


#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def AddToExceptIParr(n,value):
    l= list( ftpExceptIParr)   #  WHAT?

    num = n -l.count(value)
    for i in range(1,num):
        ftpExceptIParr.append(value)
    return

#############################################################3
# def PrepareTempFolders(config):
#     tempfolder=[]
#     for i in range(len(config.sourcefolders)):
#
#         tempfolderStr= temproot+"\\Tmp"+  "-" + config.users[i]+"-"+config.hosts[i]+"-"+ config.ports[i]
#         new_directory(tempfolderStr)
#         tempfolder.append(tempfolderStr)
#         source = config.sourcefolders[i]
#         dest = tempfolder[i]
#         copyFilesToArc(source, dest)
#     return tempfolder




    # &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

#======================================================

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
    session = namedtuple("session", "ip port user psw sourcefolder")
    config= namedtuple ("config","hosts ports users passwords sourcefolders")
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
    configProps= config(destinationHOST,port,users,passw,upfolder)

# ===== prepare temporary folders from upfolders  =====

    tempfolder = NewPrepareTempFolders(configProps,temproot)  #make and fill tempfoders() and remove upfolders
    arcfolder= CreateArcFolders(configProps,arcroot) # make arcfolder if not exist
    CopyAllFolders(tempfolder, arcfolder) #we do an arc for every user-destination

#    RemoveFromUpfolder(filedict) is in NewPrepareTempFolders
    while (continueFlag):

        ftp = FTP()

        logging.basicConfig(filename=log, level=logging.INFO, format='%(asctime)s %(message)s',
                            datefmt='%d/%m/%Y %H:%M:%S')


#===========================================================


        for i in range(len(users)):
            try:
                currentSession = session(destinationHOST[i], port[i], users[i], passw[i], tempfolder[i])
                ftpExceptIP = currentSession.user + "-" + currentSession.ip + "-" + currentSession.port

                if ( ftpExceptIP  in ftpExceptIParr) :
                    ## host was not reachable not send it
                    ftpExceptIParr.remove(ftpExceptIP)
                    time.sleep(0.25)
                else:
                    #if host was ok - send
                #    sendtempfoderFiles()
                    numsent= sendFolderFiles(currentSession)

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
        configProps = config(destinationHOST, port, users, passw, upfolder)

        tempfolder = NewPrepareTempFolders(configProps,temproot)  # make and fill tempfoders() and remove upfolders
        arcfolder = CreateArcFolders(configProps,arcroot)  # make arcfolder if not exist
        CopyAllFolders(tempfolder, arcfolder)  # we do an arc for every user-destination

