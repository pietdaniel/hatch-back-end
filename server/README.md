# todo
- everything

# done
- nothing
- basic oauth support


# dependencies

- python2
- http://tweepy.readthedocs.org/en/v3.2.0/index.html
- https://flask.pocoo.org/


# setup

First install necessary dependencies

```
pip install -r requirements.txt
```

Then, in order to keep our keys secret,
an environment variable file will need to be created.

Call this file ```ENVVAR``` and place it in ```server/```

Its format is as follows:

```
export consumer_key="PLACEHOLDER"
export consumer_secret="PLACEHOLDER"
export access_token="PLACEHOLDER"
export access_token_secret="PLACEHOLDER"
export app_secret="PLACEHOLDER"
```

Then run:

```
source ENVVAR
```

# run

```
./server/runserver.py
```



