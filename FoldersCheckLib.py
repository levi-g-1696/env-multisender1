import os.path, os


from collections import namedtuple


import smtplib, os
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
        mail.login("info@enviromanager.info", "TMerm12345!")

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


def AlertOnManyFiles(folder,num):
    message= "Warning : files number in folder " +folder+ "is " + str(num)
    send_email_to_System("Server .. multisender warning",message)
    time.sleep(1)


def MakeStatusArray (tempfolders) :
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



if __name__ == "__main__":
 #   foldersStat = namedtuple("foldersStat", "tempFolder num")  # a tuple (tempfoldr-path,
 #   tempfolders= ["C:\\Users\\wn10\\Downloads","C:\\Users\\wn10\\Downloads\\ENVR TAM 160221","C:\\Users\\wn10\\Downloads\\HMH1_20211123_1805"]
 #   status= MakeStatusArray(tempfolders)
    temproot = ".\\Temp"
    RemoveEmptyFolders(temproot)

 #   CheckTempFolderStatus(status,250)
