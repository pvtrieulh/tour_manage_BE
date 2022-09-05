# Develop environment
## Require install
```bash
1. pip install virtualenv
2. pip install virtualenvwrapper-win
```
## Build source and create new app
```bash
$ mkvirtualenv venv (venv path example: C:\Users\username\Envs) 
$ pip install -r requirement.txt
$ cd src/service/template-service 

# Optional: May be you need to run migrate db
$ python mangage.py makemigrations app_name 
$ python mangage.py migrate

# Run server
$ python mangage.py runserver

# To new app run command
$ django-admin startapp app_name
```
## Some commands needed
```bash

```