# Social Media Analysis Tool

## Development Process:

- Flask, headless REST api.

## Roles and Responsibilites:
- dj: front end, documentation
- spleensauce: front end, test automation
- pietdaniel: back end, deploys
- ali: front end, back end
- isaac: ops, back end, security

## Current Status

3.1.15
- removed client side application
- see github.com/dj/hatch

2.15.15
- server side pass one done with Flask-Login
- going to need to set up nginx from here on out, this will go server side

### Backend

- oauth 1.1 has been implemented
- this is not client side application only auth which will most likely hit rate limits
- this is per user authorization which requires server side query for security reasons
 - access_token/secret should not be sent to client side
 - client side storage of application keys is not secure
- a hack (crossdomain decorator) is used currently for testing because i dont want to set up a local nginx instance
 - this should be removed when we grab a domain/server and run with nginx
 - probably could have a better pattern here

### Frontend
- see github.com/dj/hatch

# todo
- api requirements
- api specification
- models
- authentication
- authorization

# done
- basic oauth support
- search endpoint

# dependencies

- python2
- postgres
- http://tweepy.readthedocs.org/en/v3.2.0/index.html
- https://flask.pocoo.org/
- http://initd.org/psycopg/
- http://www.sqlalchemy.org/
- http://flask-migrate.readthedocs.org/en/latest/


# setup

### set up postgres

 - for mac users: http://postgresapp.com/
 - for arch users: https://wiki.archlinux.org/index.php/PostgreSQL

 after creating a postgres user, starting the daemon, and initializing the database

 create the database.
 ```
 postgres$ createdb neuhatch
 postgres$ psql -d neuhatch
 psql (9.4.0)
 Type "help" for help.

 neuhatch=#
 ```

### set up virtualenv

http://docs.python-guide.org/en/latest/dev/virtualenvs/

#### Install
```
pip install virtualenvwrapper
```

#### Source and Create
```
source /usr/bin/virtualenvwrapper.sh
mkvirtualenv -p /usr/bin/python2 neuhatch
```

### install necessary dependencies

```
pip install -r requirements.txt
```

Note: I had issues installing on Mac osx 10.8 within a virtualenv, but installing globally worked fine

### Configure the application

Modify the configuration file in ```/instance/application.cfg```.

How to generate the app's secret key (used for securing sessions): see ["How to generate good secret keys"](http://flask.pocoo.org/docs/0.10/quickstart/#sessions).

###  initialize database and migrate the models

using ```manage.py``` initialize the database and migrate the models

```
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```

you can verify the models exist in postgres like so:

```
psql -d neuhatch
neuhatch=# \dt
```

# run

```
./runserver.py
```

# test:

Install the development requirements:

    $ pip install -r dev-requirements.txt
    $ nosetests
