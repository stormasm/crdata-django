To clean up your djangomedia directory you can
go ahead and blow away completely the directory
under djangomedia called dmvimage.

Do not touch dmvstatic.

To start from scratch you can delete your database file,
and then run the following command.

To create a database out of the box for dmv do this...
python manage.py syncdb

To make sure there are no errors.
python manage.py validate.

To bring up the development webserver run this command

cd c:\
c:\dmv\manage.py runserver
c:\dmv\manage.py runserver 131.215.12.168:7777

