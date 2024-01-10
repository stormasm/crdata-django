import rpy2.robjects as robjects
# r = robjects.r

##
#
#   R Utilities
#
##

def getuserxlimylim(request):

  xmin = request.POST['xmin']
  if(len(xmin) == 0):
    xmin = float('12345.6789')  
  else:
    xmin = float(xmin)
    
  xmax = request.POST['xmax']
  if(len(xmax) == 0):
    xmax = float('12345.6789')  
  else:
    xmax = float(xmax)

  ymin = request.POST['ymin']
  if(len(ymin) == 0):
    ymin = float('12345.6789')  
  else:
    ymin = float(ymin)

  ymax = request.POST['ymax']
  if(len(ymax) == 0):
    ymax = float('12345.6789')  
  else:
    ymax = float(ymax)

  components = [xmin,xmax,ymin,ymax]

  return(robjects.FloatVector(components))
