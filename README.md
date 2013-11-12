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
Extends the ``excel.views.Download`` and set the objs atribule with the attrs you want in you excel file.


	from excel.views import Download
	from .models import MyModel
  
	class MyDownloadPage(Download):
		objs = MyModel.objects.all()


To donwload all your database data in a single file visit:

  
	visit the ``your_projet_url/excel/database``


