# Project
This is a prototype password manager created with python.
PASSWORD MANAGER is a web application developed using Django (Python web framework) and is nothing more than a digital solution in which the user stores all their credentials and passwords in a database.

TECHNICAL PREREQUISITES AND INSTALLATION INSTRUCTIONS

To install PASSWORD MANAGER, it is important that certain conditions are met.

On the host machine, the following need to be installed:

Python
Go to https://www.python.org/downloads/ to download the executable (.exe) file of the version suitable for your system. Follow the installation steps, making sure to check the "Add Python to PATH" option during the installation.

Python dependency manager (PIP).
Go to https://bootstrap.pypa.io/get-pip.py and save the content of the page in the Python installation folder. In a terminal, navigate to the Python installation folder and run the command: 
python get-pip.py.

Django framework
Open a terminal and run the command: 
pip install django.

Allauth package (Authentication management for Django) 
Open a terminal and run the command: 
pip install django-allauth.

Allauth 2FA package (Two-factor authentication for Django)
Open a terminal and run the command: 
pip install django-allauth-2FA.

Django QR CODE package (QR code generation for Django)
Open a terminal and run the command: 
pip install django-qr-code.

Copy the project folder to a location of your choice and edit the settings.py file to configure the environment variables.

INITIALISE THE DATABASE.

SQLite 
To use SQLite database: 

- Create a file with the .sqlite3 extension (e.g., database.sqlite3) in the project folder.

- In the project folder, locate the "password_manager" and "manager" folders and open the settings.py file.

- In the DATABASES key of the settings.py file, specify the database driver, the path to the .sqlite3 file, and other required information. For example:

DATABASES = {
'default': {
  'ENGINE': 'django.db.backends.sqlite3',
  'NAME': BASE_DIR / 'database.sqlite3'
 }
}

If you want to use a database other than SQLite (e.g., Postgres, MySQL, SQL Server):

Create a file with the .sqlite3 extension (e.g., database.sqlite3) in the project folder.

In the project folder, locate the "password_manager" and "manager" subfolders and open the settings.py file.

In the DATABASES key in "settings.py" file, specify the database driver, database name, server username and password, host, and port. For example, for a Postgresql database, you'll get something like the following:

DATABASES = {
'default': {
  'ENGINE': 'django.db.backends.postgresql',
  'NAME': 'PASSWORD_MANAGER',
  'USER' : 'openpg',
  'PASSWORD' : 'openpgpwd',
  'HOST': '127.0.0.1',
  'PORT': '5432',
 }
}

After this configuration, you can initialize the database by following these steps:

Open a terminal and navigate to the project folder.

Run the following commands:

python manage.py makemigrations
python manage.py migrate
python manage.py makemigrations manager
python manage.py migrate manager


START THE PASSWORD MANAGER APPLICATION

To start the PASSWORD MANAGER application, follow these steps:

Open a terminal and navigate to the project folder.

Run the command: python manage.py runserver. You should see the following output:

Watching for file changes with StatReloader
Performing system checks...
System check identified no issues (0 silenced).
July 06, 2023 - 02:30:58
Django version 4.1.7, using settings 'password_manager.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
