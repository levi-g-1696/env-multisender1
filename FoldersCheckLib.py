import os.path, os


from collections import namedtuple


import smtplib, os,socket
import time
from  lib3 import RemoveEmptyFolders
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email_to_System(subject,text):
    try:
        # Create message container - the correct MIME type is multipart/alternative.
      #  msg = MIMEMultipart('alternative')
        msg = MIMEMultipart()
        msg['From'] = "info@enviromanager.info"
        msg['To'] = "levig.enviromanager@gmail.com"
        msg['Subject'] = subject

        msg.attach(MIMEText(text))

        mail = smtplib.SMTP("smtp.office365.com",25, timeout=20)
        mail.ehlo()
        mail.starttls()
        mail.ehlo()
        recepient = ["levig.enviromanager@gmail.com"]

      #  mail.login( "Tech1@enviromanager1.onmicrosoft.com", "TMerm12345!")
        mail.login("info@enviromanager.info", "enV-9nu&gr676")

        mail.sendmail("info@enviromanager.info", recepient, msg.as_string())

        mail.quit()

    except Exception as e:

        raise e



# def CheckUpfolderStatus(status, fileNumLimit):
#     for i in range (len(status)):
#        if status[i].num>=fileNumLimit:
#          AlertOnManyFiles(status[i].tempFolder,status[i].num)
def CheckTempFolderStatus(tempfoldersArr, fileNumLimit):
             statusArr = MakeStatusArray(tempfoldersArr)
             for i in range(len(statusArr)):
                 if statusArr[i].num >= fileNumLimit:
                     AlertOnManyFiles(statusArr[i].tempFolder,statusArr[i].num)
#============================================
def AlertToFile(file, message):
    f1 = open(file, 'a')
    timenow =  time.strftime( " %D %H:%M:%S", time.localtime())
    f1.write(timenow + " - " + message)
    f1.close()
    # ===========================================


#======================================================
def AlertOnManyFiles(folder,num, alertFile):
    message= "Warning : files number in folder " +folder+ "is " + str(num) +" \n"
    send_email_to_System("Server .. multisender warning",message)
    #  ====  append to alert file   ====
    AlertToFile(alertFile,message)
    time.sleep(3)

def AlertOnNoFolderChanged(folder,num,alertFile):
    hour= int (num/60)
    min = int (num - hour*60)
    message= " Receiving files warning  : no any changes on folder " + folder + " for " + str(hour) +" hours " + str(min) + " min\n"
    send_email_to_System("Server .. multisender warning",message)
    AlertToFile(alertFile,message)
    time.sleep(3)
def PrintLastFileAlert(file, linesNum):
    with open(file, 'r') as f:
        lines = f.read().splitlines()
    for i in range (linesNum):
        print (lines[-i-1])

def MakeStatusArray (tempfolders) :
    #counts how many files are in folder and makes tuple array
    statusArr=[]
    foldersStat = namedtuple("foldersStat", "tempFolder num")  # a tuple (tempfoldr-path,
    for folder in tempfolders:

        count = 0
        # Iterate directory
        for path in os.listdir(folder):
            # check if current path is a file
            if os.path.isfile(os.path.join(folder, path)):
                count += 1
        statusArr.append(foldersStat(folder,count))

    return statusArr


def CheckSourcefolderStatus(upfolder, receiveFilesAlertTime, alertFile):
    # alert when upfolder has no any change for <receiveFilesAlertTime> minutes
    current_time = time.time()

    for f in upfolder:
        mod_time = os.path.getmtime(f)
        noChangeTime= (current_time - mod_time) / 60
        if (noChangeTime>= receiveFilesAlertTime):
            AlertOnNoFolderChanged(f,noChangeTime,alertFile)

    return
#==========================================================================


if __name__ == "__main__":
 #   foldersStat = namedtuple("foldersStat", "tempFolder num")  # a tuple (tempfoldr-path,
 #   tempfolders= ["C:\\Users\\wn10\\Downloads","C:\\Users\\wn10\\Downloads\\ENVR TAM 160221","C:\\Users\\wn10\\Downloads\\HMH1_20211123_1805"]
 #   status= MakeStatusArray(tempfolders)

 folder2 = r"C:\Users\wn10\Downloads\HMH4_20211123_1805"
 folder1 = r"C:\Users\wn10\PycharmProjects\multisender1.0\output"
 upfo= [folder1,folder2]
 CheckSourcefolderStatus(upfo,300,".\\Alert.txt")
 PrintLastFileAlert(".\\Alert.txt",3)
 #   CheckTempFolderStatus(status,250)
