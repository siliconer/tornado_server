import json
import base64
import requests
import os
import os.path	
from starbase import Connection 
def  stargate():
	c = Connection()
	c = Connection(host='127.0.0.1', port=7060)
	print	c.tables()
#	request = requests.get(baseurl + "/" + tablename + "/schema")

stargate()
