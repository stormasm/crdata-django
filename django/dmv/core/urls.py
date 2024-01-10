
from django.conf.urls.defaults import *

urlpatterns = patterns(
    'dmv.core.views',
    (r'^$', 'home'),
    (r'^home$', 'home'),
    (r'^aboutus$', 'aboutus'),    

    (r'^userlogin$', 'userlogin'),
    (r'^userlogout$','userlogout'),
    (r'^usercreate$','usercreate'),    

    (r'^data$', 'data'),

    (r'^displayheatmap$', 'displayheatmap'),
    (r'^displayperspective$', 'displayperspective'),    
    (r'^displaycontour$', 'displaycontour'),

    (r'^displaytimeseries$', 'displaytimeseries'),
    (r'^displayplsr$', 'displayplsr'),
    (r'^displaypca$', 'displaypca'),
    (r'^displayjqueryui$', 'displayjqueryui'),
    (r'^displayrotateaxes$', 'displayrotateaxes'),    
    (r'^displaybarchart$', 'displaybarchart'),
    (r'^displaypiechart$', 'displaypiechart'),
    (r'^displayboxplot$',  'displayboxplot'),
    (r'^displaymds$', 'displaymds'),
    
    (r'^dataupload$', 'dataupload'),
    
    (r'^dataview$', 'dataview'),
    (r'^dataedit$', 'dataedit'),
    (r'^datadelete$', 'datadelete'),

    (r'^analysis$', 'analysis'),
    (r'^analysistimeseries$', 'analysistimeseries'),
    (r'^analysisplsr$', 'analysisplsr'),
    (r'^analysispca$', 'analysispca'),
    (r'^analysisjqueryui$', 'analysisjqueryui'),
    (r'^analysisrotateaxes$','analysisrotateaxes'),    
    (r'^analysispiechart$', 'analysispiechart'),
    (r'^analysisbarchart$', 'analysisbarchart'),
    (r'^analysisboxplot$',  'analysisboxplot'),        
    (r'^analysismds$', 'analysismds'),

    (r'^analysiscontour$', 'analysiscontour'),
    (r'^analysisperspective$', 'analysisperspective'),
    (r'^analysisheatmap$', 'analysisheatmap'),    
    
    (r'^helptop$', 'helptop'),
    (r'^helppageone$', 'helppageone'),
    (r'^helppagetwo$', 'helppagetwo'),
    (r'^helppagethree$', 'helppagethree'),
    (r'^helppagefour$', 'helppagefour'),
    (r'^helppagefive$', 'helppagefive'),            

    (r'^gallery$', 'gallery'),
    (r'^gallerydelete$', 'gallerydelete'),
    (r'^galleryone$', 'galleryone'),
    (r'^gallerytwo$', 'gallerytwo'),

    # Ajax calls

    (r'^ajaxgetdatafromfilerowcol$', 'ajaxgetdatafromfilerowcol'),
    (r'^ajaxgetdatafromfile$', 'ajaxgetdatafromfile'),
    (r'^ajaxgetrownamesfromfile$', 'ajaxgetrownamesfromfile'),
    (r'^ajaxgetcolumnnamesfromfile$', 'ajaxgetcolumnnamesfromfile'),    
    (r'^ajaxgetnumberofcolumnsfromfile$', 'ajaxgetnumberofcolumnsfromfile'),    
    (r'^ajaxtest$', 'ajaxtest'),
    
    )

urlpatterns += patterns('dmv.core.viewsinteractive',

    (r'^interactive$', 'interactive'),
    (r'^interactivedelete$', 'interactivedelete'),
    (r'^interactiveone$', 'interactiveone'),
    (r'^interactivetwo$', 'interactivetwo'),

    (r'^analysisinteractivemds$', 'analysisinteractivemds'),
    (r'^interactivemds$', 'interactivemds'),                        
)
