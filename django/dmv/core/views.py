import logging
import math
import os
import pdb
import re

from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.http import HttpResponseForbidden, HttpResponseNotFound
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.utils import simplejson

import django.template

## local global named functions
from sortcompare import natsorted
from rowcolumnutil import getRowNameFromRow, processRowNames, processRowsColumns
from rutil import getuserxlimylim

## local classes
from models import DataUpload, Sequence
from plot import ReadFile, ReadFileWriteTab, PlotOne, PlotRotateAxis, PlotPCA, PlotPlsr, InteractiveData
from datatablesutil import DataTablesUtil
from filetype import FileType

import istore

##
#
#   Global Variables
#
##

# Counter displayed (by respond()) below) on every page showing how
# many requests the current incarnation has handled, not counting
# redirects.  Rendered by templates/base.html.

counter = 0

##
#
#   Forms
#
##

class NewForm(forms.Form):  
  data = forms.FileField()
  filetype = forms.ChoiceField(choices=[('Type001', 'Type001')])
  modelname = forms.ChoiceField(choices=[('Multivariate', 'Multivariate')])

##
#
#   Custom respond function
#
##

def respond(request, template, params=None):
  """
  Helper to render a response, passing standard stuff to the response.

  Args:
    request: The request object.
    template: The template name; '.html' is appended automatically.
    params: A dict giving the template parameters; modified in-place.

  Returns:
    Whatever render_to_response(template, params) returns.

  Raises:
    Whatever render_to_response(template, params) raises.
  """
  
  global counter
  counter += 1
  if params is None:
    params = {}

  params['request'] = request
  params['anonymoususer'] = request.user.is_authenticated()
  params['counter'] = counter
  params['user'] = request.user

  try:
    return render_to_response(template, params)
  except AssertionError:
    logging.exception('AssertionError')
    return HttpResponse('AssertionError')

##
#
#   Request Handlers
#
##

##
#
#   Home
#
##

def home(request):
  return respond(request, 'home.html')

def aboutus(request):
  return respond(request, 'aboutus.html')

##
#
#   Analysis
#
##

def analysis(request):
  return respond(request, 'analysis.html')

def analysisbarchart(request):
    data = processAnalysisRowColumnRequestData(request)
    files = data[0]
    if files == []:
      return respond(request, 'datashownofiles.html')
    rownames = data[1]
    columnnames = data[2]
    return respond(request, 'analysisbarchart.html',
              {'files':files,'rownames':rownames,'columnnames':columnnames,})

def analysispiechart(request):
    data = processAnalysisRowColumnRequestData(request)
    files = data[0]
    if files == []:
      return respond(request, 'datashownofiles.html')
    rownames = data[1]
    columnnames = data[2]
    return respond(request, 'analysispiechart.html',
              {'files':files,'rownames':rownames,'columnnames':columnnames,})

def analysistimeseries(request):
    data = processAnalysisRowColumnRequestData(request)
    files = data[0]
    if files == []:
      return respond(request, 'datashownofiles.html')                 
    rownames = data[1]
    columnnames = data[2]
    return respond(request, 'analysistimeseries.html',
              {'files':files,'rownames':rownames,'columnnames':columnnames,})

def analysisheatmap(request):
    data = processAnalysisRowColumnRequestData(request)
    files = data[0]
    if files == []:
      return respond(request, 'datashownofiles.html')                 
    rownames = data[1]
    columnnames = data[2] 
    return respond(request, 'analysisheatmap.html',
              {'files':files,'rownames':rownames,'columnnames':columnnames,})

def analysisboxplot(request):
    data = processAnalysisRowColumnRequestData(request)
    files = data[0]
    if files == []:
      return respond(request, 'datashownofiles.html')                 
    rownames = data[1]
    columnnames = data[2]
    return respond(request, 'analysisboxplot.html',
              {'files':files,'rownames':rownames,'columnnames':columnnames,})

def analysismds(request):
    data = processAnalysisRowColumnRequestData(request)
    files = data[0]
    if files == []:
      return respond(request, 'datashownofiles.html')
    rownames = data[1]
    columnnames = data[2]
    return respond(request, 'analysismds.html',
              {'files':files,'rownames':rownames,'columnnames':columnnames,})

def analysisplsr(request):
    files = processAnalysisRequestData(request)
    if files == []:
      return respond(request, 'datashownofiles.html')
    return respond(request, 'analysisplsr.html',
              {'files':files})

def analysispca(request):
    files = processAnalysisRequestData(request)
    if files == []:
      return respond(request, 'datashownofiles.html')
    return respond(request, 'analysispca.html',
              {'files':files})

  
##
#
#   Display
#
##

def displaybarchart(request):
  data = processDisplayRequestData(request,'BarChart-')
  rows = data[0]
  columns = data[1]
  dataLocator = data[2]
  imageLocator = data[3]
  imageDisplayName = data[4]
  palettename = data[5]
  plot = PlotOne()  
  plot.plotbarchart(rows,columns,dataLocator,imageLocator,palettename)
  return respond(request, 'displayplot.html', {'generatedfile':imageDisplayName})

def displaypiechart(request):
  data = processDisplayRequestData(request,'PieChart-')
  rows = data[0]
  columns = data[1]
  dataLocator = data[2]
  imageLocator = data[3]
  imageDisplayName = data[4]  
  palettename = data[5]
  plot = PlotOne()  
  plot.plotpiechart(rows,columns,dataLocator,imageLocator,palettename)
  return respond(request, 'displayplot.html', {'generatedfile':imageDisplayName})

def displaytimeseries(request):
  data = processDisplayRequestData(request,'TimeSeries-')
  rows = data[0]
  columns = data[1]
  dataLocator = data[2]
  imageLocator = data[3]
  imageDisplayName = data[4]
  palettename = data[5]  
  plot = PlotOne()  
  plot.plottimeseries(rows,columns,dataLocator,imageLocator,palettename)
  return respond(request, 'displayplot.html', {'generatedfile':imageDisplayName})

def displayheatmap(request):
  data = processDisplayRequestData(request,'HeatMap-')
  rows = data[0]
  columns = data[1]
  dataLocator = data[2]
  imageLocator = data[3]
  imageDisplayName = data[4]
  palettename = data[5]  
  plot = PlotOne()  
  plot.plotheatmap(rows,columns,dataLocator,imageLocator,palettename)
  return respond(request, 'displayplot.html', {'generatedfile':imageDisplayName})

def displayboxplot(request):
  data = processDisplayRequestData(request,'BoxPlot-')
  rows = data[0]
  columns = data[1]
  dataLocator = data[2]
  imageLocator = data[3]
  imageDisplayName = data[4]
  palettename = data[5]  
  plot = PlotOne()  
  plot.plotboxplot(rows,columns,dataLocator,imageLocator,palettename)
  return respond(request, 'displayplot.html', {'generatedfile':imageDisplayName})

def displaymds(request):
  datakeys = request.POST.keys()

  ## for axis scaling

  xyamount = request.POST['xyamount']
  xyamount = float(xyamount)
  gamma = xyamount / 10.0

  logscale = ""
  
  if("logscale" in datakeys):
    logscale = "xy"

  userxlimylim = getuserxlimylim(request)

  # same as above with this one extra line
  distype = request.POST['distancemeasure']
  
  data = processDisplayRequestDataNoPalette(request,'MDS-')
  rows = data[0]
  columns = data[1]
  dataLocator = data[2]
  imageLocator = data[3]
  imageDisplayName = data[4]
  interactiveLocator = data[5]
  interactiveDisplayName = data[6]

  ## for axis rotation

  xamount = request.POST['xamount']
  xamount = float(xamount)
  theta = math.radians(xamount)
  
  plot = PlotOne()  
  plot.plotmds(rows,columns,dataLocator,imageLocator,distype,theta,gamma,logscale,userxlimylim)

  interactive = InteractiveData()
  interactive.interactivemds(rows,columns,dataLocator,interactiveLocator,distype)

  return respond(request, 'displayplotandinteractive.html',
                 {'generatedfile':imageDisplayName,'interactivefile':interactiveDisplayName})

def displaypca(request):
  datakeys = request.POST.keys()
  textoutput = False
  
  if("textoutput" in datakeys):
    textoutput = True

  # For Axis Rotation
  xamount = request.POST['xamount']
  xamount = float(xamount)
  theta = math.radians(xamount)

  # For axis scaling

  logscale = ""
  
  if("logscale" in datakeys):
    logscale = "xy"

  userxlimylim = getuserxlimylim(request)

  xyamount = request.POST['xyamount']
  xyamount = float(xyamount)
  gamma = xyamount / 10.0

  data = processDisplayRequestDataNoPalette(request,'PCA-')
  rows = data[0]
  columns = data[1]
  dataLocator = data[2]
  imageLocator = data[3]
  imageDisplayName = data[4]
  interactiveLocator = data[5]
  interactiveDisplayName = data[6]
  
  plot = PlotPCA()
  plot.plot(dataLocator,imageLocator,interactiveLocator,textoutput,theta,gamma,logscale,userxlimylim)
  
  return respond(request, 'displayplotandinteractive.html',
                 {'generatedfile':imageDisplayName,'interactivefile':interactiveDisplayName})

def displayplsr(request):

  textoutput = False
  data = request.POST
  username = getUserName(request)
  filename1 = data['filename1']
  filename2 = data['filename2']
  component1 = data['group1']
  component2 = data['group2']
  plsCompPlot = [component1,component2]

  datakeys = data.keys()

  if("textoutput" in datakeys):
    textoutput = True

  ## for axis rotation

  xamount = request.POST['xamount']
  xamount = float(xamount)
  theta = math.radians(xamount)

  ## for axis scaling

  logscale = ""
  
  if("logscale" in datakeys):
    logscale = "xy"

  userxlimylim = getuserxlimylim(request)

  xyamount = request.POST['xyamount']
  xyamount = float(xyamount)
  gamma = xyamount / 10.0
  
  # Set up imageLocator

  filePrefix = os.path.splitext(filename1)
  uniquenumber = istore.getNextSequenceNumber()

  imageDisplayName = 'Plsr-' + filePrefix[0] + '-' + str(uniquenumber) + ".png"
  imageLocator = istore.getImageLocation(username) + imageDisplayName

  # Set up dataLocator

  datadict = istore.readDataDictionaryFromDatastore(username,filename1)
  dataLocator1 = istore.readDictionaryAndGenerateRandomFile(datadict,username)

  datadict = istore.readDataDictionaryFromDatastore(username,filename2)
  dataLocator2 = istore.readDictionaryAndGenerateRandomFile(datadict,username)

  # Set up the interactiveLocator and the interactiveDisplayName

  analysisName = 'Plsr-'

  interactiveDisplayName = analysisName + filePrefix[0] + '-' + str(uniquenumber) + ".csv"
  interactiveLocator = istore.getInteractiveLocation(username) + interactiveDisplayName

  plot = PlotPlsr()
  plot.plot(dataLocator1,dataLocator2,imageLocator,interactiveLocator,plsCompPlot,textoutput,theta,gamma,logscale,userxlimylim)

  return respond(request, 'displayplotandinteractive.html',
                 {'generatedfile':imageDisplayName,'interactivefile':interactiveDisplayName})
  
##
#
#   Helper Functions
#
##

def processDisplayRequestData(request,analysisName):

  username = getUserName(request)
  
  # This is a Django QueryDict
  data = request.POST
  filename = data['filename']
  
  # Pass in a Django QueryDict and
  # Return a normal Python dictionary with two lists[rows and columns]
  dictrowcolumn = processRowsColumns(data)
  rows = dictrowcolumn['rows']
  columns = dictrowcolumn['columns']

  # Set up imageLocator

  filePrefix = os.path.splitext(filename)
  uniquenumber = istore.getNextSequenceNumber()

  imageDisplayName = analysisName + filePrefix[0] + '-' + str(uniquenumber) + ".png"
  imageLocator = istore.getImageLocation(username) + imageDisplayName

  # Set up dataLocator

  datadict = istore.readDataDictionaryFromDatastore(username,filename)
  dataLocator = istore.readDictionaryAndGenerateRandomFile(datadict,username)

  palette = data['palette']

  return([rows,columns,dataLocator,imageLocator,imageDisplayName,palette])


#
# If we always passed in a palette by default
# for MDS and PCA then we wouldn't need this
# extra method for NoPalette
#
def processDisplayRequestDataNoPalette(request,analysisName):

  username = getUserName(request)
  
  # This is a Django QueryDict
  data = request.POST
  filename = data['filename']
  
  # Pass in a Django QueryDict and
  # Return a normal Python dictionary with two lists[rows and columns]
  dictrowcolumn = processRowsColumns(data)
  rows = dictrowcolumn['rows']
  columns = dictrowcolumn['columns']

  # Set up imageLocator
  filePrefix = os.path.splitext(filename)
  uniquenumber = istore.getNextSequenceNumber()

  imageDisplayName = analysisName + filePrefix[0] + '-' + str(uniquenumber) + ".png"
  imageLocator = istore.getImageLocation(username) + imageDisplayName

  # Set up dataLocator
  datadict = istore.readDataDictionaryFromDatastore(username,filename)
  dataLocator = istore.readDictionaryAndGenerateRandomFile(datadict,username)

  # Set up interactiveLocator

  interactiveDisplayName = analysisName + filePrefix[0] + '-' + str(uniquenumber) + ".csv"
  interactiveLocator = istore.getInteractiveLocation(username) + interactiveDisplayName

  return([rows,columns,dataLocator,imageLocator,imageDisplayName,interactiveLocator,interactiveDisplayName])

def processAnalysisRequestData(request):
    username = getUserName(request)
    files = istore.readAllFileNamesForModelFromDatastore(username,'Multivariate')
    if files == []:
      return files
    files = natsorted(files)
    return files

def processAnalysisRowColumnRequestData(request):
    username = getUserName(request)
    files = istore.readAllFileNamesForModelFromDatastore(username,'Multivariate')
    if files == []:
      return([files])      
    files = natsorted(files)
    rownames = istore.getRowNamesFromDatastore(username, files[0])
    columnnames = istore.getColumnNamesFromDatastore(username, files[0])
    columnnames = columnnames[1:]
    return([files,rownames,columnnames])

##
#
#   Data Upload
#
##

def data(request):
  return respond(request, 'data.html')

def dataupload(request):
  username = getUserName(request)
  if request.method == 'POST':
    form = NewForm(request.POST, request.FILES)
    if form.is_valid():

      filetypexternal = form.cleaned_data['filetype']
      modelname = form.cleaned_data['modelname']      

      istore.createUsernameLocations(username)
      filenamelist = writeUploadedFileToTmpDirectory(request)

      if len(filenamelist) != 2:
        logging.error('This should never happen, Throw an Exception')

      uploadedFilename = filenamelist[0]
      uploadedFilename = istore.getTmpDirFromCwd() + uploadedFilename

      tmpFilename = filenamelist[1]
##    logging.error(tmpFilename)

      results = dataUploadCheck(tmpFilename)

      if results['pass'] == True:

        filetype = FileType()
        filetype = filetype.getFileType(tmpFilename)

        ### Create a tab delimited file using R from the uploaded file

        readFileWriteTab = ReadFileWriteTab()
        readFileWriteTab.readFileWriteTab(tmpFilename,uploadedFilename,filetype)
        datadictionary = istore.readLinesIntoDictionary(uploadedFilename)
        uploadedFilename = os.path.basename(uploadedFilename)
        istore.writeDataDictionaryToDatastore(username,uploadedFilename,datadictionary,filetypexternal,modelname)
        return respond(request, 'datauploadsuccess.html')        
      else:
        errors = results['errors']
        return respond(request, 'datauploaderror.html', {'errors': errors})        
  else:
    form = NewForm()
  return respond(request, 'dataupload.html', {'form': form})

def writeUploadedFileToTmpDirectory(request):

  # This line is here for the case when you click on the show(data) link
  # and you are NOT actually doing a data upload in that particular case
  # so you just want to blast out of this method and not actually execute it

  if not(request.FILES.has_key('data')):
   return []

  uploadedfile = request.FILES['data']  
  filenamelist = istore.writeFileToTmpDirectory(uploadedfile,getUserName(request))
  return filenamelist

def dataUploadCheck(tmpfilename):

  filetype = FileType()
  filetype = filetype.getFileType(tmpfilename)
  testReadingFile = ReadFile()
  results = {}
  try:
    testReadingFile.read(tmpfilename, filetype)
    results['pass'] = True
  except Exception, inst:
    results = buildResults(results, inst)
    results['pass'] = False
  return results

def buildResults(results, inst):
  errors = []
  for errorstrings in inst:
    errors.append(errorstrings)
  results['errors'] = errors
  return results

##
#
#   Data View Edit Delete
#
##

def dataview(request):
    username = getUserName(request)
    files = istore.readAllFileNamesForModelFromDatastore(username,'Multivariate')
    if files == []:
      return respond(request, 'datashownofiles.html')
    files = natsorted(files)
    genenames = istore.getRowNamesFromDatastore(username, files[0])
    return respond(request, 'dataview.html',
              {'files':files,'genenames':genenames,})

def dataedit(request):
  return respond(request, 'dataedit.html')

def datadelete(request):
  username = getUserName(request)
  if request.method == 'POST':
    filenames = request.POST   
    filenames = filenames.keys()
    
    for b in filenames:
      if b != 'example_length':
        a = DataUpload.objects.filter(filename=b)
        a.delete()

  files = istore.readAllFileNamesFromDatastore(username)
  return respond(request, 'datadelete.html', {'files':files})  

##
#
#   Login / Logout
#
##

def userlogin(request):
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
      if user.is_active:
        django.contrib.auth.login(request, user)
        return respond(request, 'helppageone.html')
  return respond(request, 'userlogin.html')

def userlogout(request):
  django.contrib.auth.logout(request)
  return respond(request, 'userlogout.html')

def usercreate(request):
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      form.save()
      return respond(request, 'home.html')
  else:
    form = UserCreationForm()
  return respond(request, 'usercreate.html', {'form': form})

##
#
#   Help
#
##

def helptop(request):
  return respond(request, 'help.html')

def helppageone(request):
  return respond(request, 'helppageone.html')

def helppagetwo(request):
  return respond(request, 'helppagetwo.html')

def helppagethree(request):
  return respond(request, 'helppagethree.html')

def helppagefour(request):
  return respond(request, 'helppagefour.html')

def helppagefive(request):
  return respond(request, 'helppagefive.html')


##
#
#   Gallery
#
##

def gallery(request):
  return respond(request,'gallery.html')

def gallerydelete(request):
    username = getUserName(request)
    imageDirectory = istore.getImageLocation(username)
    if(os.path.exists(imageDirectory) == False):
      return respond(request, 'datashownoimages.html')                 

    if request.method == 'POST':
      filenames = request.POST
      filenames = filenames.keys()
      
      for b in filenames:
        if b != 'example_length':
          os.remove(imageDirectory + os.sep + b)
  
    files = os.listdir(imageDirectory)
    files = natsorted(files)
    return respond(request, 'gallerydelete.html',{'files':files})

def galleryone(request):

  username = getUserName(request)   
  imageDirectory = istore.getImageLocation(getUserName(request))
  if(os.path.exists(imageDirectory) == False):
    return respond(request, 'datashownoimages.html')                 

  files = os.listdir(imageDirectory)
  files = natsorted(files)
  return respond(request, 'galleryone.html', {'files':files})  

def gallerytwo(request):

  username = getUserName(request)
  imageDirectory = istore.getImageLocation(getUserName(request))
  if(os.path.exists(imageDirectory) == False):
    return respond(request, 'datashownoimages.html')                 

  files = os.listdir(imageDirectory)
  files = natsorted(files) 
  return respond(request, 'gallerytwo.html', {'files':files})  

##
#
#   Utilities -- we have decided to leave these here
#
##

def getUserName(request):
  if request.user.username == "":
    return "AnonymousUser"
  return request.user.username


##
#
#   Ajax
#
##

def ajaxtest(request):
    html = "<html><body>hi</body></html>"
    return HttpResponse(html)

def ajaxgetrownamesfromfile(request):

    username = getUserName(request)
    filename = request.POST['filename']
    data = istore.readDataDictionaryFromDatastore(username,filename)
    datavalues = data.values()
    genenames = {}
    count = 0
    for row in datavalues[1:]:
      name = getRowNameFromRow(row)
      genenames[count] = name
      count = count + 1
    return HttpResponse(simplejson.dumps(genenames))

def ajaxgetcolumnnamesfromfile(request):

    username = getUserName(request)
    filename = request.POST['filename']
    data = istore.readDataDictionaryFromDatastore(username,filename)
    datavalues = data.values()
    columns = datavalues[0]
    columns = re.split("\s",columns)
    columnames = {}
    count = 0
    for column in columns[1:]:
      columnames[count] = column
      count = count + 1
    return HttpResponse(simplejson.dumps(columnames))

def ajaxgetnumberofcolumnsfromfile(request):

    username = getUserName(request)
    filenames = request.POST

    # See the Django documenation for the QueryDict methods
    filename1 = filenames.getlist('filename1')
    filename2 = filenames.getlist('filename2')

    filename1 = str(filename1[0])
    filename2 = str(filename2[0])
  
    data1 = istore.readDataDictionaryFromDatastore(username,filename1)
    data2 = istore.readDataDictionaryFromDatastore(username,filename2)

    data1values = data1.values()
    columns1 = data1values[0]
    columns1 = re.split("\s",columns1)    
    file1columns = len(columns1) - 1
 
    data2values = data2.values()
    columns2 = data2values[0]
    columns2 = re.split("\s",columns2)    
    file2columns = len(columns2) - 1

    ddict = {}
    
    if(file1columns == file2columns):
        ddict['check'] = file1columns
    else:
        ddict['check'] = 0

    return HttpResponse(simplejson.dumps(ddict))  

def ajaxgetdatafromfile(request):

    username = getUserName(request)
    filename = request.POST['filename']
    data = istore.readDataDictionaryFromDatastore(username,filename)
    columnames = istore.getColumnNamesFromDatastore(username, filename)
    dtu = DataTablesUtil()
    ddict = {}
    ddict['aaData'] = dtu.convertDataFileToDict(data)
    ddict['aoColumns'] = dtu.convertColumnListToDict(columnames)
    datajson = dtu.replacesTitle(str(ddict))
    return HttpResponse(datajson)

def ajaxgetdatafromfilerowcol(request):

    username = getUserName(request)
    filename = request.POST['filename']
    data = istore.readDataDictionaryFromDatastore(username,filename)
    return HttpResponse(simplejson.dumps(data))

##
#
#   Eventually these routines need to be refactored and/or removed
#
##

def analysisrotateaxes(request):

    username = getUserName(request)
    files = istore.readAllFileNamesForModelFromDatastore(username,'Multivariate')
    if files == []:
      return respond(request, 'datashownofiles.html')
    files = natsorted(files)
    genenames = istore.getRowNamesFromDatastore(username, files[0])
    return respond(request, 'analysisrotateaxes.html',
              {'files':files,'genenames':genenames,})

def analysisjqueryui(request):

    username = getUserName(request)
    files = istore.readAllFileNamesForModelFromDatastore(username,'Multivariate')
    if files == []:
      return respond(request, 'datashownofiles.html')
    files = natsorted(files)
    genenames = istore.getRowNamesFromDatastore(username, files[0])
    return respond(request, 'analysisjqueryui.html',
              {'files':files,'genenames':genenames,})

def analysisperspective(request):
    data = processAnalysisRowColumnRequestData(request)
    files = data[0]
    if files == []:
      return respond(request, 'datashownofiles.html')                 
    rownames = data[1]
    columnnames = data[2]
    return respond(request, 'analysisperspective.html',
              {'files':files,'rownames':rownames,'columnnames':columnnames,})

def analysiscontour(request):
    data = processAnalysisRowColumnRequestData(request)
    files = data[0]
    if files == []:
      return respond(request, 'datashownofiles.html')                 
    rownames = data[1]
    columnnames = data[2]
    return respond(request, 'analysiscontour.html',
              {'files':files,'rownames':rownames,'columnnames':columnnames,})

def displayrotateaxes(request):
# same as above routines with these three extra lines
  xamount = request.POST['xamount']
  xamount = float(xamount)
  xamount = math.radians(xamount)
  
  data = processDisplayRequestData(request,'RotateAxis-')
  rows = data[0]
  columns = data[1]
  dataLocator = data[2]
  imageLocator = data[3]
  imageDisplayName = data[4]  
  plot = PlotRotateAxis()  
  plot.plotrotateaxis(dataLocator,imageLocator,xamount)
  return respond(request, 'displayplot.html', {'generatedfile':imageDisplayName})

def displayperspective(request):
  data = processDisplayRequestData(request,'Perspective-')
  rows = data[0]
  columns = data[1]
  dataLocator = data[2]
  imageLocator = data[3]
  imageDisplayName = data[4]  
  plot = PlotOne()  
  plot.plotperspective(rows,columns,dataLocator,imageLocator)
  return respond(request, 'displayplot.html', {'generatedfile':imageDisplayName})

def displayjqueryui(request):
  return respond(request, 'displayplot.html')

# currently NOT being used
def displaycontour(request):
  return respond(request, 'displayplot.html')
