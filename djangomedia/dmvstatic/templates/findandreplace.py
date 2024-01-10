import os

class Engine():

    def findAndReplace(self,filename):
        fp = FileProcessor()
        fp.findandreplace(filename)
    
class FileProcessor():

    def findandreplace(self,filename):
        f = open(filename)
        text = f.read()
        f.close()
        f = open(filename,"w")
## 1) What we have
## 2) What we want it to be

#       LOJA / CRDATA
        f.write(text.replace('http://loja.caltech.edu','http://www.crdata.org'))
#       f.write(text.replace('http://www.crdata.org','http://loja.caltech.edu'))
#       LOJA / ARGON
#       f.write(text.replace('http://loja.caltech.edu','http://argon.caltech.edu'))
#       LOCALHOST
#       Deals with localhost
#       f.write(text.replace('http://loja.caltech.edu','http://localhost'))
#       f.write(text.replace('http://localhost','http://ec2-75-101-145-144.compute-1.amazonaws.com'))
#       f.write(text.replace('http://localhost','http://loja.caltech.edu'))

        f.close()
        return True

#engine = Engine()
#filename = 'tone\\analysisbarchart.html'
#engine.findAndReplace(filename)

## given a directory name this program will
## read each individual file and check to make
## sure the file can be read by R

class AutoReadDirectory():

    def readMultipleFilesFromDirectory(self,directory):

        files = self.getListOfFilesInDirectory(directory)

        for file in files:
            datafile = directory + file
            print("reading " + datafile)
            engine = Engine()
            engine.findAndReplace(datafile)
            
        print("We have completed reading all of the files in " + directory)

    ## only return actual files, skip over directories

    def getListOfFilesInDirectory(self,dirname):
        tmplistoffiles = os.listdir(dirname)
        listoffiles = []
        for afile in tmplistoffiles:
            if(not os.path.isdir(dirname + afile)):
                listoffiles.append(afile)
        return listoffiles
        
def run():
    directories = ['./core/','./interactive/']
#   directories = ['./core/']
    x = AutoReadDirectory()
    for directory in directories:
        x.readMultipleFilesFromDirectory(directory)

run()
