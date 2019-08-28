#!/usr/bin/python

import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/cloudsek/")
sys.path.insert(1,"/var/www/cloudsek/cloudsek")
from tas import app as application
application.secret_key = 'Add your secret key'




