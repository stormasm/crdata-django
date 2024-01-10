import logging
import pickle
import re

from datetime import datetime

# Local
from models import DataUpload, Sequence
import rowcolumnutil

##
#
#   Reading and Writing to the Database
#
##

class databaseutil():

    def getNextSequenceNumber(self):
      a = Sequence.objects.all()
      if len(a) == 0:
        b = Sequence(filenumber = '0')
        b.save()
        return 0
      c = Sequence.objects.order_by('filenumber')[0]
      nextnumber = c.filenumber + 1
      c.filenumber = nextnumber
      c.save()
      return nextnumber

    # returns all of the filenames in a list filtered by user
    def readAllFileNamesFromDatabase(self,username):
      filenames = []
      a = DataUpload.objects.filter(username=username)
      for b in a.iterator():
    #   filenames.append(b.filename)
        filenames.append(b)
      return filenames

    # returns all of the filenames in a list filtered by user and model
    def readAllFileNamesForModelFromDatabase(self,username,modelname):
      filenames = []
      a = DataUpload.objects.filter(username=username,modelname=modelname)
      for b in a.iterator():
        filenames.append(b.filename)
      return filenames

    def readDataDictionaryFromDatabase(self,username,datafilename):
      a = DataUpload.objects.filter(filename=datafilename,username=username)
      for b in a.iterator():
        dataDictionary = pickle.loads(str(b.pickledictionary))
      return dataDictionary

    def writeDataDictionaryToDatabase(self,username,datafilename,datadictionary,filetype,modelname):

      mypickle=str(pickle.dumps(datadictionary))

      # If the file already exists then simply update the file
      a = DataUpload.objects.filter(filename=datafilename,username=username)
      # Changed so that you can't get the same file name with 2 different models
      # Now you should not have 2 files with the same name and different models

      if a.count() == 0:
        b = DataUpload(id=None, username = username, filename=datafilename, filetype=filetype, filedate=datetime.today(), pickledictionary = mypickle, modelname=modelname)
        b.save()
        logging.info('Created a new file with id = ', b.id)
      else:
        if a.count() > 1:
          # We need to figure out how to throw an Exception here
          logging.error('Dmv System Error view.py: should not have more than 1 file with the same name')
        else:
          for b in a.iterator():
            b.pickledictionary = mypickle
            b.filetype = filetype
            b.filedate=datetime.today()
            b.save()
            
    def getRowNamesFromDatabase(self, username, filename):

        data = self.readDataDictionaryFromDatabase(username,filename)
        datavalues = data.values()
        genenames = []

        for row in datavalues[1:]:
          name = rowcolumnutil.getRowNameFromRow(row)
          genenames.append(name)

        return genenames

    def getColumnNamesFromDatabase(self, username, filename):

        data = self.readDataDictionaryFromDatabase(username,filename)
        datavalues = data.values()

        # get the first row which is the columns
        columnames = datavalues[0]
        columnames = rowcolumnutil.getListFromRow(columnames)
#       columnames = columnames[1:]

        return columnames
