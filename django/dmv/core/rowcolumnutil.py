import re

def getRowNameFromRow(row):
  result = re.split("\s",row)
  return result[0]

def getListFromRow(row):
  result = re.split("\s",row)
  return result

# pass in a dictionary and return a list of genenames
# the filename is easy to get so don't need to worry about that
def processRowNames(data):
  genenames = []
  keys = data.keys()
  for key in keys:
    if key != "filename":
      genenames.append(data[key])
  return genenames

# pass in a Django QueryDict and process the rows and columns
def processRowsColumns(data):

  # See the Django documenation for the QueryDict methods
  rows = data.getlist('row')
  columns = data.getlist('column')

  mydict = {}
  mydict['rows'] = rows
  mydict['columns'] = columns

  return mydict
