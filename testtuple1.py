import time

from tsttupfile import tsttup

from collections import namedtuple
from  lib2 import confreader,copyFilesToArc,Remove1File,RemoveFilesFrom, removeOld,copyFilesFromList
import os.path, os



#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
def PrepareTempFolders(config):
    tempfolder=[]
    for i in range(len(config.sourcefolders)):

        tempfolderStr= temproot+"\\Tmp"+  "-" + config.users[i]+"-"+config.hosts[i]+"-"+ config.ports[i]
        new_directory(tempfolderStr)
        tempfolder.append(tempfolderStr)
        source = config.sourcefolders[i]
        dest = tempfolder[i]
        copyFilesToArc(source, dest)
    return tempfolder

def new_directory(directory):
  # Before creating a new directory, check to see if it already exists

  if os.path.isdir(directory) == False:
    os.makedirs(directory)
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
#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
def MakeUpfolderDictionary(upfolder):

    upFolderDict = {}
    emptyArr=[]
    for i in range (len(upfolder)):
        upFolderDict[upfolder[i]]=emptyArr
    for key,val in upFolderDict.items():
        upFolderDict[key] = GetFileList(key)

    return  upFolderDict
    # &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
def NewPrepareTempFolders(config):
    tempfolder = []
    print ("making upfolder dictionary")
    upFolderDict=MakeUpfolderDictionary(upfolder)

    for i in range(len(upfolder)):
        tempfolderStr= temproot+"\\Tmp"+  "-" + config.users[i]+"-"+config.hosts[i]+"-"+ config.ports[i]
        new_directory(tempfolderStr)
        tempfolder.append(tempfolderStr) #??? do we need it?
        print("copying to tempfolder ",tempfolderStr)
        key= config.sourcefolders[i]
        fileList = upFolderDict[key]
        copyFilesFromList(fileList, tempfolderStr) ###########must check



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
#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&


temproot = ".\\Temp"
configFile = ".\\transferConfig22.csv"

isEnable, isLastDest, users, passw, upfolder, destinationHOST, port = confreader(configFile)
updict= MakeUpfolderDictionary(upfolder)

print (updict)
time.sleep(12)
RemoveFromUpfolder(upfolderDict=updict)
    # Adding list as value
 #   myDict["key1"] = [1, 2]
#  MakeUpfolderDictionary:
#     {
#     make dict keys (key= upfolder[i])
#     fill using function GetFileList(key) value= list of files in this folder at the moment
#     }
#     /* GetFileList(key) returns string array local file paths. so every key has value an array
#  --------------------------------
#  NewPrepareTempFolders(upfolder):  /*the old tool gets session props. makes unical path for this ses. makes folder if it
                                   #/*   does not exist. Copies file from upfolders to tempfolder. returns nothing/
                                   #/* here we have to do the same but the copiying must be by file list stored in dictionary
#    MakeUpfolderDictionary
#    for all upfolders:
#      {
#      Make Tempfolder (unical) if does not exist
#      get fileList from dictionary by upfolder key
#       copy all files to current tempfolder
#      }
#
#
#-------------------------------------------
#RemoveFromUpfolder
#   for all keys UpfolderDictionary:
#     { delete files by list on  current key value}
#
#
#
#
#