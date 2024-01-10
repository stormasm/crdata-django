import logging
import os
import random
import time

## interface classes
import dirutil
from databaseutil import databaseutil
databaseutil = databaseutil()

#
#
#  These are the databaseutil calls
#
#

def writeDataDictionaryToDatastore(username,uploadedFilename,datadictionary,filetypexternal,modelname):
        return databaseutil.writeDataDictionaryToDatabase(username,uploadedFilename,datadictionary,filetypexternal,modelname)

def getNextSequenceNumber():
        return databaseutil.getNextSequenceNumber()

def readAllFileNamesFromDatastore(username):
        return databaseutil.readAllFileNamesFromDatabase(username)

def getRowNamesFromDatastore(username,filename):
        return databaseutil.getRowNamesFromDatabase(username, filename)

def getColumnNamesFromDatastore(username,filename):
        return databaseutil.getColumnNamesFromDatabase(username, filename)

def readAllFileNamesForModelFromDatastore(username,model):
        return databaseutil.readAllFileNamesForModelFromDatabase(username,model)

def readDataDictionaryFromDatastore(username,filename):
        return databaseutil.readDataDictionaryFromDatabase(username,filename)

#
#
#  These are the dirutil calls
#
#

def getImageLocation(username):
        return dirutil.getImageDirectory(username)

def getInteractiveLocation(username):
        return dirutil.getInteractiveDirectory(username)

def createUsernameLocations(username):
        return dirutil.createUsernameDirectories(username)

# this takes a dictionary and generates a random file
# and returns the file name

def readDictionaryAndGenerateRandomFile(data,username):

        tmpstart = getTmpDirFromCwd()
        tmpstop = tmpstart + getRandomFileName(username)
        tmpfile = open(tmpstop,'w')

        for key,value in data.items():
            tmpfile.write(value)
            tmpfile.write('\n')

        tmpfile.close()          

        return tmpfile.name

# this takes a string as file pointer and returns a dictionary
def readLinesIntoDictionary(filename):

        count = 0
        data = {}

        f = open(filename)
          
        # start with the column header line
        for row in f.readlines():   
              line = row.strip()
              data[count] = line
              count = count + 1

        f.close()          
        return data

def getRandomFileName(username):
        timefloat = time.time()
        timename = str(timefloat)
        index = timename.find('.')
        timenew = timename.replace('.','q')
        randomnew = str(random.randint(1,1000000))
        timeplusrandom = timenew + randomnew
        zname = 'z' + timeplusrandom[4:-1]
        zname = username + zname
        return zname

def writeFileToTmpDirectory(uploadedfile,username):

      ### Get a random file name
      tmpfilename = getTmpDirFromCwd() + getRandomFileName(username)

      uploadedfile.open()
      tmpfile = open(tmpfilename,'w')

      for chunk in uploadedfile.chunks():
        tmpfile.write(chunk)

      tmpfile.close()
      uploadedfile.close()
      return [uploadedfile.name, tmpfilename]
    
def getTmpDirFromCwd():
        # this was the old way, leave here for awhile for reference
        # basedirectory = os.getcwd()
        basedirectory = os.sep + 'tmp'        
        tmpdirectory = basedirectory + os.sep + 'dmv' + os.sep
        if (os.path.exists(tmpdirectory) == False):
            os.mkdir(tmpdirectory)
        return tmpdirectory
