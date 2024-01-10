import os
from django.shortcuts import render_to_response

## local global named functions
from sortcompare import natsorted
from plot import InteractiveData
from rowcolumnutil import processRowsColumns
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
#   Gallery
#
##

def interactive(request):
  return respond(request,'interactive.html')

def interactivedelete(request):
    username = getUserName(request)
    interactiveDirectory = istore.getInteractiveLocation(username)

    if request.method == 'POST':
      filenames = request.POST
      filenames = filenames.keys()
      
      for b in filenames:
        if b != 'example_length':
          os.remove(interactiveDirectory + os.sep + b)
  
    files = os.listdir(interactiveDirectory)
    files = natsorted(files)
    return respond(request, 'interactivedelete.html',{'files':files})

def interactivemds(request):

  # This is a Django QueryDict
  data = request.POST
  filename = data['filename']
  distype = data['distancemeasure']
  username = getUserName(request)
  
  # Pass in a Django QueryDict and
  # Return a normal Python dictionary with two lists[rows and columns]
  dictrowcolumn = processRowsColumns(data)
  rows = dictrowcolumn['rows']
  columns = dictrowcolumn['columns']
  
  # Set up interactiveLocator

  filePrefix = os.path.splitext(filename)
  uniquenumber = istore.getNextSequenceNumber()

  imageDisplayName = 'Mds-' + filePrefix[0] + '-' + str(uniquenumber) + ".csv"
  interactiveLocator = istore.getInteractiveLocation(username) + imageDisplayName

  # Set up dataLocator

  datadict = istore.readDataDictionaryFromDatastore(username,filename)
  dataLocator = istore.readDictionaryAndGenerateRandomFile(datadict,username)

  interactive = InteractiveData()
  interactive.interactivemds(rows,columns,dataLocator,interactiveLocator,distype)
  
  return respond(request, 'interactivemds.html', {'generatedfile':imageDisplayName})

def interactiveone(request):

  username = getUserName(request)   
  interactiveDirectory = istore.getInteractiveLocation(username)
  files = os.listdir(interactiveDirectory)
  files = natsorted(files) 
  return respond(request, 'interactiveone.html', {'files':files})  

def interactivetwo(request):

  username = getUserName(request)   
  interactiveDirectory = istore.getInteractiveLocation(username)
  files = os.listdir(interactiveDirectory)
  files = natsorted(files) 
  return respond(request, 'interactivetwo.html', {'files':files})  

def analysisinteractivemds(request):
    data = processAnalysisRowColumnRequestData(request)
    files = data[0]
    rownames = data[1]
    columnnames = data[2]
    return respond(request, 'analysisinteractivemds.html',
              {'files':files,'rownames':rownames,'columnnames':columnnames,})

def processAnalysisRequestData(request):
    username = getUserName(request)
    files = istore.readAllFileNamesForModelFromDatastore(username,'Multivariate')
    if files == []:
      return respond(request, 'datashownofiles.html')
    files = natsorted(files)
    return files

def processAnalysisRowColumnRequestData(request):
    username = getUserName(request)
    files = processAnalysisRequestData(request)
    rownames = istore.getRowNamesFromDatastore(username, files[0])
    columnnames = istore.getColumnNamesFromDatastore(username, files[0])
    columnnames = columnnames[1:]
    return([files,rownames,columnnames])
  
##
#
#   Utilities -- we have decided to leave these here
#
##

def getUserName(request):
  if request.user.username == "":
    return "AnonymousUser"
  return request.user.username

