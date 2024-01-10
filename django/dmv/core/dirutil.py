import os

##
#
#   Directory and Filename Global Functions
#
##

def getImageDirectory(username):
  imageDirectory = getTemplateDirectory("image",username)
  return imageDirectory

def getInteractiveDirectory(username):
  interactiveDirectory = getTemplateDirectory("interactive",username)
  return interactiveDirectory

def getTemplateDirectory(dirname, username):
  directory = getTopLevelDirectory() + username + os.sep + dirname + os.sep
  return directory

def getTopLevelDirectory():
  if (os.name == 'nt'):
    topLevelDirectory = os.sep + "mnt" + os.sep + "store" + os.sep + "djangomedia" + os.sep + "dmvimage" + os.sep
  else:
    topLevelDirectory = "/mnt/store/djangomedia" + os.sep + "dmvimage" + os.sep
  return topLevelDirectory

def createUsernameDirectories(username):
    direxists = userDirectoryExists(username)

    if direxists != True:
      imageDirectory = getImageDirectory(username)
      os.makedirs(imageDirectory)
      interactiveDirectory = getInteractiveDirectory(username)
      os.makedirs(interactiveDirectory)
      
def userDirectoryExists(username):
    imageDirectory = getImageDirectory(username)
    direxists = os.path.exists(imageDirectory)
    return direxists
