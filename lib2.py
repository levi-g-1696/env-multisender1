#################################################################
def new_directory(directory):
  # Before creating a new directory, check to see if it already exists

  if os.path.isdir(directory) == False:
    os.makedirs(directory)

#############################################################3
def MakeTempFolders():
    for i in range(len(upfolder)):

        tempfolderStr= temproot+"\\Tmp"+  "-" + users[i]+"-"+destinationHOST[i]+"-"+port[i]
        new_directory(tempfolderStr)
        tempfolder.append(tempfolderStr)
        source = upfolder[i]
        dest = tempfolder[i]

