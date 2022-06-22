# This is a sample Python script.

import os.path, os
from ftplib import FTP, error_perm
from shutil import copy2
import csv
from  lib1 import confreader,copyFilesToArc,Remove1File,RemoveFilesFrom, removeOld
import logging
import time, ftplib, glob
import subprocess



# MMMMMMMMMMMMMMMMMM  MAIN  MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
# error on lof file is busy/ have to make new file
configFile = ".\\transferConfig2.csv"
log = ".\\Log\\transferLog.csv"

logoldpath = ".\\LogOld\\"
ftpExceptIP = ""
ftpExceptEscapecount = 30
st = "c:\\ftpTransfer\\stop.conf"
#=============================================================================

if __name__ == "__main__":
    ## stoping option  ##

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
    isEnable,isLastDest, users, passw, upfolder, arcfolder, \
    destinationHOST, port, tempfolder = confreader(configFile)

    while (continueFlag):

        ftp = FTP()

        logging.basicConfig(filename=log, level=logging.INFO, format='%(asctime)s %(message)s',
                            datefmt='%d/%m/%Y %H:%M:%S')

  # ===== prepare temporary folders from upfolders  =====
        for i in range(len(upfolder)):
            source = upfolder[i]
            dest = tempfolder[i]

            if (source != "No"):
                copyFilesToArc(source, dest)
#===========================================================
        for i in range(len(users)):
            try:
                if (ftpExceptIP == destinationHOST[i]) & (ftpExceptEscapecount > 0):
                    ftpExceptEscapecount = ftpExceptEscapecount - 1
                else:
                    # copyFilesToArc(upfolder[i], arcfolder[i])
                #    print(" Prepare Sending FTP to  ", destinationHOST[i], "by user ", users[i])

                    ftp.connect(destinationHOST[i], int(port[i]))
                    ftp.login(users[i], passw[i])


                    tempFolderPath = tempfolder[i]
                    upFolderPath = upfolder[i]
               #     print("prepare list for ftp, path :", tempFolderPath)
                    numsent=0
                    for name in os.listdir(tempFolderPath):

                        localpath = os.path.join(tempFolderPath, name)



                        if os.path.isfile(localpath):
                            ftp.storbinary('STOR ' + name, open(localpath, 'rb'))
                            numsent= numsent+1
                           # print("placefile FTP  ", localpath)
                            time.sleep(0.03)
                            if upFolderPath != "No":
                                localpathUpfolder = os.path.join(upFolderPath, name)
                                Remove1File(localpathUpfolder)
                        else:
                            print("main, 208,source content error")
                    logging.info("," + destinationHOST[i] + "," + users[i] + "," + upfolder[i])
                    print( "  ", numsent , " files were sent to " ,destinationHOST[i], users[i])
                    ftp.quit()

            except ftplib.all_errors as e:
                print(" \n> > > >   F T P exception  - ", destinationHOST[i], users[i],str(e),"\n")

                time.sleep(0.5)
                ftpExceptIP = destinationHOST[i]
                ftpExceptEscapecount = 10
                logging.info("," + destinationHOST[i] + "," + users[i] + "," + upfolder[i] + "," + "Error " + str(e))
        time.sleep(0.45)
 # &&&&&&&&   tempfolders to archive   &&&&&&&&&&&&&&&&&&&&&&&&&&7
        for i in range(len(upfolder)):
            if upfolder[i] != "No":
                source = tempfolder[i]
                dest = arcfolder[i]
                copyFilesToArc(source, dest)
#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
        time.sleep(0.45)

        for i in range(len(upfolder)):
            if upfolder[i] != "No":
                RemoveFilesFrom(tempfolder[i])

        print()
        print()
        print("        *******************************************")
        print("        *        ENVIRO MULTISENDER 5.17          *")
        print("        *   file transfer     is running          *")
        print("        *        DO NOT CLOSE THIS WINDOW         *")
        print("        *******************************************")
        print("        *\n\r    paz a stacks files are moving by system schedual tool \n")

        j = j + 1
        m = m + 1
        if m % 18 == 0:  # every 3 min
            # BatchRemoveOlderThan_15min()
            m = 0
        if j % 6 == 0:
            removeOld()  # every 1 min

            #  log= makeNewLogFile(log)

            j = 0
        else:
            time.sleep(10)
        ##  check stop   ##
        lines = tuple(open(st, 'r'))
        arr = lines[0].split("=")
        if "1" in arr[1]:
            continueFlag = False
