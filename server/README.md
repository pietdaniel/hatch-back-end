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
- http://www.sqlalchemy.org/http://www.sqlalchemy.org/
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

```
source /usr/bin/virtualenvwrapper.sh
mkvirtualenv -p /usr/bin/python2 neuhatch
```

### install necessary dependencies

```
pip install -r requirements.txt
```

### export environment variables

in order to keep our keys secret, an environment variable file will need to be created.

Call this file ```ENVVAR``` and place it in ```server/```

Its format is as follows:

```
export consumer_key="PLACEHOLDER"
export consumer_secret="PLACEHOLDER"
export access_token="PLACEHOLDER"
export access_token_secret="PLACEHOLDER"
export app_secret="PLACEHOLDER"
export database_url="postgres://localhost/neuhatch"
```

Then run:

```
source ENVVAR
```

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
./server/runserver.py
```



