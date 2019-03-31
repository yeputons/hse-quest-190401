#!/usr/bin/env python3
from flask import Flask, render_template
from bank import Bank

def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_pyfile(config_filename)

    @app.route('/')
    def index():
        return render_template('index.html2')

    return app
