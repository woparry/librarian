#!/bin/env python
# -*- coding: utf-8 -*-
'''
lookup a product using its upc
Example: https://api.upcitemdb.com/prod/trial/lookup?upc=5035822011717
'''
import requests
import json
import logging
from datetime import datetime
logging.basicConfig(level=logging.DEBUG, format='%(module)s: LINE %(lineno)d: %(levelname)s: %(message)s')
DEBUG = logging.debug

class UPCLookup(object):
    def get_response(self, upc):
        ''' Get and test the response.
        @param The url of the request.
        @return The response.
        '''
        url = "https://api.upcitemdb.com/prod/trial/lookup?upc="
        retries = 2 # Try this many times
        while retries:
            r = requests.get(url + upc)
            if r.status_code == 200:
                return r
            retries -= 1
        return None

    def get_product(self, upc):
        r = lookup.get_response(upc)
        return r.json()




if __name__ == '__main__':
    lookup = UPCLookup()
    r = lookup.get_response("5035822011717")
    print json.dumps(r.json(), indent=2, sort_keys=True)
