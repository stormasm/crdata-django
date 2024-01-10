import re

class DataTablesUtil():

    def convertColumnListToDict(self,columnlist):
        mylist = []
        index = 0
        for item in columnlist:
            x = dict()
            sTitle = "sTitle-" + str(index)
            x[sTitle] = item
            mylist.append(x)
            index = index + 1
        return(mylist)

    def getListFromRow(self,row):
        result = re.split("\s",row)
        return result

    def replacesTitle(self,string):
        result = re.sub("sTitle-\d","sTitle",string)
        return result
    
    def convertDataFileToDict(self,data):
        d = {}
        mylist = []
        for row in data:
            if row > 0:
                mylist.append(self.getListFromRow(data[row]))
        return(mylist)

    def testrun():
        why = ['A','B','C']
        test = DataTablesUtil()
        d = test.convertColumnListToDict(why)
        d = str(d)
        print(test.replacesTitle(d))

