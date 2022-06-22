
import os.path, os
from ftplib import FTP, error_perm
from shutil import copy2
import csv
from  lib1 import confreader,copyFilesToArc,Remove1File,RemoveFilesFrom, removeOld
import logging
import time, ftplib, glob
import subprocess

def sendTempFolderFiles1(destinationHOST,port,tempFolderPath,user,psw):
    ftp = FTP()
    ftp.connect(destinationHOST, int(port))
    ftp.login(user, psw)


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
                print("  ===> F T P exception on sending " , fileLocalpath, " user ", user, " to ", destinationHOST)
        else:
            print("main, 208,source content error")
    ftp.quit()
    return numsent

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
