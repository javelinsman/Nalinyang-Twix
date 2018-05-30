"""
Interface to receive messages from Telegram
"""

import threading
import logging
import json

import requests
import bot_config

from basic.database_wrapper_redis import DatabaseWrapperRedis

from flask import Flask, request


class InterfaceEmorecViewer(threading.Thread):
    "This class is for viewing emorec data on the web"
    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port
        self.db = DatabaseWrapperRedis(host=bot_config.DB_HOST, #pylint: disable=invalid-name
                                       port=bot_config.DB_PORT, db=bot_config.DB_NUM)

        self.app = Flask(__name__)
        @self.app.route("/", methods=['GET', 'POST'])
        def index():
            return "Hello"

        @self.app.route("/shutdown", methods=['GET', 'POST'])
        def shutdown(): #pylint: disable=unused-variable
            "shutdown the Flask server"
            func = request.environ.get('werkzeug.server.shutdown')
            if func is not None:
                func()
            return ''

    def run(self):
        self.app.run(host=self.host, port=self.port, debug=False)
    def shutdown(self):
        "sends http request to Flask server to call '/shutdown' inside"
        logging.debug('shutdown()')
        requests.get('http://%s:%s/shutdown' % (self.host, self.port))
