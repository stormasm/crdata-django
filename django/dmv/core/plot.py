import logging
import os
import rpy2.robjects as robjects
from filetype import FileType
import istore

r = robjects.r

def buildUrl(rfile):
    if (os.name == 'nt'):
        part1 = "http://loja.caltech.edu/dmvstatic/r/"
#       part1 = "http://localhost/dmvstatic/r/"        
    else:
        part1 = "http://www.crdata.org/dmvstatic/r/"        
#   part1 = "http://ec2-75-101-145-144.compute-1.amazonaws.com/dmvstatic/r/"
    url = part1 + rfile
    return(url)

class ReadFile():

    def read(self,filenameData,fileType):
        filename = buildUrl("readrfile.txt")
        r.source(file=filename)
        r.readfile(datafile=filenameData,filetype=fileType)

class ReadFileWriteTab():

    def readFileWriteTab(self,inputfile,outputfile,fileType):
        filename = buildUrl("readrfilewritetab.txt")
        r.source(file=filename)
        r.readfilewritetab(inputfile=inputfile,outputfile=outputfile,filetype=fileType)

class PlotOne():

    def plotbarchart(self,rows,columns,dataLocator,imageLocator,palette):
        url = buildUrl("rowcolumn.txt")
        r.source(file=url)
        url = buildUrl("color.txt")
        r.source(file=url)
        url = buildUrl("barchart.txt")
        r.source(file=url)
        filetype = FileType()
        filetype = filetype.getFileType(dataLocator)
        robjects.globalEnv["palettename"] = palette
        r.plotbarchart(rownames=rows,columnnames=columns,datafile=dataLocator,imagefile=imageLocator,filetype=filetype)

    def plotpiechart(self,rows,columns,dataLocator,imageLocator,palette):
        url = buildUrl("rowcolumn.txt")
        r.source(file=url)
        url = buildUrl("color.txt")
        r.source(file=url)
        url = buildUrl("piechart.txt")
        r.source(file=url)
        filetype = FileType()
        filetype = filetype.getFileType(dataLocator)
        robjects.globalEnv["palettename"] = palette        
        r.plotpiechart(rownames=rows,columnnames=columns,datafile=dataLocator,imagefile=imageLocator,filetype=filetype)

    def plottimeseries(self,rows,columns,dataLocator,imageLocator,palette):
        url = buildUrl("rowcolumn.txt")
        r.source(file=url)
        url = buildUrl("color.txt")
        r.source(file=url)        
        url = buildUrl("timeseries.txt")
        r.source(file=url)
        filetype = FileType()
        filetype = filetype.getFileType(dataLocator)
        robjects.globalEnv["palettename"] = palette        
        r.plottimeseries(rownames=rows,columnnames=columns,datafile=dataLocator,imagefile=imageLocator,filetype=filetype)

    def plotheatmap(self,rows,columns,dataLocator,imageLocator,palette):
        url = buildUrl("rowcolumn.txt")
        r.source(file=url)
        url = buildUrl("color.txt")
        r.source(file=url)        
        url = buildUrl("heatmap.txt")
        r.source(file=url)
        filetype = FileType()
        filetype = filetype.getFileType(dataLocator)
        robjects.globalEnv["palettename"] = palette        
        r.plotheatmap(rownames=rows,columnnames=columns,datafile=dataLocator,imagefile=imageLocator,filetype=filetype)

    def plotboxplot(self,rows,columns,dataLocator,imageLocator,palette):
        url = buildUrl("rowcolumn.txt")
        r.source(file=url)
        url = buildUrl("color.txt")
        r.source(file=url)        
        url = buildUrl("boxplot.txt")
        r.source(file=url)
        filetype = FileType()
        filetype = filetype.getFileType(dataLocator)
        robjects.globalEnv["palettename"] = palette        
        r.plotboxplot(rownames=rows,columnnames=columns,datafile=dataLocator,imagefile=imageLocator,filetype=filetype)

    def plotmds(self,rows,columns,dataLocator,imageLocator,distype,
                theta,gamma,logscale,userxlimylim):
        url = buildUrl("rowcolumn.txt")
        r.source(file=url)
        url = buildUrl("xlimylim.txt")
        r.source(file=url)
        url = buildUrl("mds.txt")
        r.source(file=url)
        filetype = FileType()
        filetype = filetype.getFileType(dataLocator)  
        r.plotmds(rownames=rows,columnnames=columns,datafile=dataLocator,
                  imagefile=imageLocator,filetype=filetype,distype=distype,
                  theta=theta,gamma=gamma,logscale=logscale,userxlimylim=userxlimylim)

    def plotperspective(self,rows,columns,dataLocator,imageLocator):
        url = buildUrl("rowcolumn.txt")
        r.source(file=url)
        url = buildUrl("perspective.txt")
        r.source(file=url)
        filetype = FileType()
        filetype = filetype.getFileType(dataLocator)  
        r.plotperspective(imagefile=imageLocator)

class PlotPCA():

    def plot(self,dataLocator,imageLocator,interactiveLocator,outfilebool,theta,gamma,logscale,userxlimylim):
        url = buildUrl("xlimylim.txt")
        r.source(file=url)
        url = buildUrl("pca.txt")
        r.source(file=url)
        outfile = istore.getTmpDirFromCwd() + os.sep + 'princomp.txt'
        filetype = FileType()
        filetype = filetype.getFileType(dataLocator)        
        r.plotpca(datafile=dataLocator,imagefile=imageLocator,interactivefile=interactiveLocator,filetype=filetype,outfile=outfile,outfilebool=outfilebool,theta=theta,gamma=gamma,logscale=logscale,userxlimylim=userxlimylim)
        
class PlotPlsr():

    def plot(self,dataLocator1,dataLocator2,imageLocator,interactiveLocator,twocomponents,outfilebool,theta,gamma,logscale,userxlimylim):
        url = buildUrl("xlimylim.txt")
        r.source(file=url)
        url = buildUrl("pls.txt")
        r.source(file=url)
        outfile = istore.getTmpDirFromCwd() + os.sep + 'pnas.txt'
        filetype = FileType()
        filetype1 = filetype.getFileType(dataLocator1)        
        filetype2 = filetype.getFileType(dataLocator2)        
        plsCompPlot = robjects.IntVector(twocomponents)
        r.plotpls(datafile1=dataLocator1,datafile2=dataLocator2,imagefile=imageLocator,interactivefile=interactiveLocator,filetype1=filetype1,filetype2=filetype2,outfile=outfile,plsCompPlot=plsCompPlot,outfilebool=outfilebool,theta=theta,gamma=gamma,logscale=logscale,userxlimylim=userxlimylim)
        
class InteractiveData():

    def interactivemds(self,rows,columns,dataLocator,imageLocator,distype):
        url = buildUrl("rowcolumn.txt")
        r.source(file=url)
        url = buildUrl("mdsinteractive.txt")
        r.source(file=url)
        filetype = FileType()
        filetype = filetype.getFileType(dataLocator)  
        r.interactivecmdscale(rownames=rows,columnnames=columns,datafile=dataLocator,imagefile=imageLocator,filetype=filetype,distype=distype)

class PlotRotateAxis():
    
    def plotrotateaxis(self,dataLocator,imageLocator,theta):
        url = buildUrl("axisrotate.txt")
        r.source(file=url)        
        filetype = FileType()
        filetype = filetype.getFileType(dataLocator)
        r.plotsimple(datafile=dataLocator,imagefile=imageLocator,filetype=filetype,theta=theta)
