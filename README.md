Django excel
============
Django excel is an app to create Excel files

Install
-----
Add ``excel`` in your ``INSTALLED_APPS``::


	INSTALLED_APPS = (
	...
	'excel',
	)

	
Configuration
-----
Bind the ``djang-excel`` ``urls.py`` into your main ``urls.py`` with something like:


  url(r'^excel/', include('excel.urls')),
 
  
Usage
----
A single objects list::


  from excel.views import Download
  from .models import MyModel
  
  class MyDownloadPage(Download):
      objs = MyModel.objects.all()


The Database::

  
  visit the ``your_projet_url/excel/database``


