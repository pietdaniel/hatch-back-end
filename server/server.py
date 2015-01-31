#!/usr/bin/env python2
from flask import Flask
app = Flask(__name__)

@app.route('/smoke')
def smoke_Test():
    return True

if __name__ == '__main__':
    app.run()
