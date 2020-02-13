=====
refs
=====

refs is a Django application to create references for scientific databases. 
The goal of the app is to create a referencing system where an administrator need only enter the Digital Object Identifier (DOI)
of an article and in return get the full citation of the aforementioned article. 
This system is setup to output references in HTML, BibTeX and JSON format with the following information from the article:
The citations in this notebook are retrieving the following information on a paper: Title, Authors, Journal Name, Volume Number, Page Range, Year, Hyperlink(s) to the Article and DOI of the Article.

Detailed Setup
-----------
1. Set up your local_settings.py file.

    Include your Secret_Key in Secret_Key = : This is used to provide cryptographic signing, and should be set to a unique, unpredictable value.
django-admin startproject automatically adds a randomly-generated SECRET_KEY to each new project.
Uses of the key shouldn’t assume that it’s text or bytes. 
Every use should go through force_str() or force_bytes() to convert it to the desired type.
Django will refuse to start if SECRET_KEY is not set.

    Setup your database information: An example is shown below,
    DATABASES = 
    'default': 
        'ENGINE': 'django.db.backends.postgresql',
        
        'NAME': 'mydatabase',
        
        'USER': 'mydatabaseuser',
        
        'PASSWORD': 'mypassword',
        
        'HOST': '127.0.0.1',
        
        'PORT': '5432',

    More information on how to setup your settings.py file can be found here: https://docs.djangoproject.com/en/3.0/ref/settings/
    
2. Setup your conf.py file.

    webapp_path = os.path.join('/Users/user_name/name_of_file') 
    
    In the above webapp_path information you should change user_name to your user name listed on your computer.
    file_name is the name of the file where the refs django application is stored.

3. Create your environment and upload the required modules and packages. A good reference for this step is at https://tutorial.djangogirls.org/en/django_installation/

    Execute the following in your command line (for windows users) other users please refer to the link above
    
        cd file_name 
        
        python -m venv myvenv 
        
        myvenv\\Scripts\\activate
        
        pip install -r requirements.txt 
        
        python manage.py migrate 
        
        python manage.py runserver 

Notes:

            *S in Scripts is capitalized

            *file_name is the file where this django application is stored

            *myvenv is the created virtual environment, you can call it any name, here I chose myvenv

            *you may need to manually install mysqlclient 1.4.4, django 1.11 and requests 2.22, and for windows you may need the binary file 'mysqlclient-1.4.4-64_or_32_bit.whl' which can be found online (commonly on university websites)

            *after you complete runserver step, copy and paste the http generated link, in the webpage and upon reaching the refs page enter your doi press enter and observe your generated reference!
            
            *depending on your database setup, upon pasting the link and reaching the webpage you may be prompted to enter a username and password. If you encounter problems with access to the refs webpage then run "python manage.py createsuperuser" this is a quick fix to the issue. 
