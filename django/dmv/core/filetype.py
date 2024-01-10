import re
import fileinput

'''

Any time this file gets modified it will
be modified here -- and not any where else.

20090403a -- two core interfaces up and running...

This function call returns one of the following
three strings {csv, tab, space}
filetype.getFileType(filename)

This function call returns a data structure which
can then be further parsed

filetype.getData(filename)

This class works on two main data structures.
lineinfo and brain

lineinfo is the first pass
it simply adds up all of the different things found on a line
and accumlates that data across the file

once that information has been compiled

then the second pass is to build up the brain datastructure

while doing this if at any point in time a criticalproblem
it detected then then all processing ceases and the user
is alerted immediately with the most logical issue they
need to deal with.

once the brain datastructure is completed
then a final decision is made and passed back to the
calling program.

If the user needs to be alerted to a problem then that happens also.

This class returns a file type {tab, space, csv}
if it figures out what kind of file the user or uploaded
or a reason telling the user to modify the file

There are also boolean functions for the file type
'''

class FileType():

# strings that could some day eventually be internationalized

# critical problems
    criticalproblem00 = 'Number of Lines in your file is Zero'
# problems
    problem00 = 'No problem'
# filetypes
    filetypecsv = 'csv'
    filetypetab = 'tab'
    filetypespace = 'space'
    filetypeunknown = 'unknown'

    brain = [0,0,0,0]

    reason = {'filetype' : 'default-filetype',
              'critical' : False,
              'problem' : 'default-problem'}

    lineinfo = {'linecountabs' : 0,
            'linecountspaces' : 0,
            'linecountcommas' : 0,
            'numberoflines' : 0}

    def init(self):
        self.lineinfo['linecountabs'] = 0
        self.lineinfo['linecountspaces'] = 0
        self.lineinfo['linecountcommas'] = 0
        self.lineinfo['numberoflines'] = 0
        self.reason['filetype'] = 'default-filetype'
        self.reason['critical'] = False
        self.reason['problem'] = 'default-problem'

    def readFileProcess(self,filename):
        f = open(filename)
        count = 0
        try:
            for line in f:
                self.process(line,self.lineinfo)
                count = count + 1
        finally:
                f.close()
        self.lineinfo['numberoflines'] = count - 1                
        return self.lineinfo

    def readLineProcess(self,lines):
        for line in lines:
            self.process(line,self.lineinfo)
        return self.lineinfo

    def process(self,wholefile,info):
        
        value = self.numberOfTotalTabsInFile(wholefile)
        if type(value) == int:
            self.lineinfo['linecountabs'] = self.lineinfo['linecountabs'] + value

        value = self.numberOfTotalCommasInFile(wholefile)
        if type(value) == int:
            self.lineinfo['linecountcommas'] = self.lineinfo['linecountcommas'] + value

        value = self.numberOfTotalLinesInFile(wholefile)
        if type(value) == int:
            self.lineinfo['numberoflines'] = self.lineinfo['numberoflines'] + value
            
    def numberOfTotalLinesInFile(self,line):
        p = re.compile('\n')
        instances = p.findall(line)
        return len(instances)

    def numberOfTotalTabsInFile(self,line):
        p = re.compile('\t')
        instances = p.findall(line)
        return len(instances)

    def numberOfTotalCommasInFile(self,line):
        p = re.compile(',')
        instances = p.findall(line)
        return len(instances)

#    Leave this here for the forseeable future
#    through the end of 2009 to show how to do
#    the search function in re, or until
#    search is actually implemented somewhere in this class
#
#    def checkForTabDelimitedLines(self,line):
#        if re.search('\t',line):
#            return 1

    # this file processes the lineinfo datastructure
    # and creates the brain datastructure based on the lineinfo

    def testForCriticalProblems(self):
        numoflines = self.lineinfo['numberoflines']
        numofcommas = self.lineinfo['linecountcommas']
        if numoflines <= 1:
            self.reason['critical'] = True
            self.reason['problem'] = self.criticalproblem00
            self.reason['filetype'] = self.filetypeunknown
            return True
        
    def testForCsv(self):
        numoflines = self.lineinfo['numberoflines']
        numofcommas = self.lineinfo['linecountcommas']
#       print 'numofcommas ', numofcommas
#       print 'numoflines ', numoflines
        if numofcommas > (numoflines - 3):
            self.reason['problem'] = self.problem00
            self.reason['filetype'] = self.filetypecsv
            return True
        return False

    def testForTab(self):
        numoflines = self.lineinfo['numberoflines']
        numoftabs = self.lineinfo['linecountabs']
        if numoftabs > (numoflines - 3):
            self.reason['problem'] = self.problem00
            self.reason['filetype'] = self.filetypetab
            return True
        return False

    # If the file has no tabs and no commas, then
    # for now I believe we can assume it is pure spaces
    def testForNotTabOrCsv(self):
        numoflines = self.lineinfo['numberoflines']
        numofcommas = self.lineinfo['linecountabs']
        numoftabs = self.lineinfo['linecountabs']
        if (numofcommas == 0) & (numoftabs == 0):
            self.reason['problem'] = self.problem00
            self.reason['filetype'] = self.filetypespace
            return True
        return False

    def processInfoDataStructure(self):
        # check to see if it is a csv file first
        # if a file is csv then we are probably in pretty good shape
        # so finish processing by returning that you got a filetype
        # numoflines = self.info['numberoflines']
        # numofcommas = self.info['linecountcommas']
        #
        #
        # brain[0,0,0,0] means file is unknown, send back diagnosis
        # brain[0,0,0,1] means file is space
        # brain[0,0,1,0] means file is tab
        # brain[0,1,0,0] means file is csv
        # brain[0,1,1,0] means file is csv and tab
        # brain[1,1,1,1] means file has a problem, send back diagnosis
        if self.testForCriticalProblems():
            return self.reason            
        if self.testForCsv():
            return self.reason
        if self.testForTab():
            return self.reason
        if self.testForNotTabOrCsv():
            return self.reason

    def getFileTypeFixed(self,lines):
        self.init()
        datalineinfo = self.readLineProcess(lines)
        datareason = self.processInfoDataStructure()
        return datareason

    # this function returns a string denoting
    # to the best approximation what kind of file type
    # the user has uploaded

    def getFileType(self,filename):
        fof = FixOddFiles()

        if(fof.strangefile(filename)):
            fixedlines = fof.process(filename)
            return self.getFileTypeFixed(fixedlines)['filetype']
        
        f = open(filename)
        lines = f.read()
        f.close()
        return self.getFileTypeFixed(lines)['filetype']


    def getData(self,filename):
        fof = FixOddFiles()

        if(fof.strangefile(filename)):
            fixedlines = fof.process(filename)
            return self.getFileTypeFixed(fixedlines)
        
        f = open(filename)
        lines = f.read()
        f.close()
        return self.getFileTypeFixed(lines)

    
class FixOddFiles():

    def strangefile(self,filename):
        f = open(filename)
        lines1 = f.read()
        size1 = len(lines1)
        
        g = open(filename)
        lines2 = g.readline()
        size2 = len(lines2)

        f.close()
        g.close()

        if size1 == size2:
            return True
        return False
    
    def numberOfCarriageReturns(self,line):
        p = re.compile('\r')
        instances = p.findall(line)
        return len(instances)

    def numberOfLineFeeds(self,line):
        p = re.compile('\n')
        instances = p.findall(line)
        return len(instances)

    def numberOfCarriageReturnLineFeeds(self,line):
        p = re.compile('\r\n')
        instances = p.findall(line)
        return len(instances)

    def replaceCarriageReturnWithLineFeed(self,filename):        
        f = open(filename)
        lines = f.read()
        lines = (str(lines))
        lines = lines.replace('\r','\n')
        return lines

    def process(self,filename):
        if(self.strangefile(filename)):
            f = open(filename)
            lines = f.read()
            carriagereturns = self.numberOfCarriageReturns(lines)
            linefeeds = self.numberOfLineFeeds(lines)
            carriagereturnlinefeeds = self.numberOfCarriageReturnLineFeeds(lines)
            if(carriagereturns > linefeeds & carriagereturnlinefeeds == linefeeds):
                fixedlines = self.replaceCarriageReturnWithLineFeed(filename)
                return fixedlines

'''
filetype = FileType()
filename = 'data\\twins.csv'
print(filetype.getFileType(filename))
filename = 'data\\filetypecsv.txt'
print(filetype.getFileType(filename))
filename = 'data\\filetypecsv-nospaces.txt'
print(filetype.getFileType(filename))
filename = 'data\\filetypespace.txt'
print(filetype.getFileType(filename))
filename = 'data\\filetypetab.txt'
print(filetype.getFileType(filename))

filename = 'data\\twins.csv'
print(filetype.getData(filename))
filename = 'data\\filetypecsv.txt'
print(filetype.getData(filename))
filename = 'data\\filetypecsv-nospaces.txt'
print(filetype.getData(filename))
filename = 'data\\filetypespace.txt'
print(filetype.getData(filename))
filename = 'data\\filetypetab.txt'
print(filetype.getData(filename))
'''
