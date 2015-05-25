import json
import base64
import requests
import os
import os.path	
from commands import *

from starbase import Connection 
def  stargate():
	c = Connection()
	c = Connection(host='127.0.0.1', port=7060)
	print	c.tables()
#	request = requests.get(baseurl + "/" + tablename + "/schema")
	count_cmd = '/usr/bin/hbase org.apache.hadoop.hbase.mapreduce.RowCounter SRR1514737  read'
	text = getoutput(cmd)
	print text
	rowkey = 200000
	print 'row key '
	t = c.table('SRR1514737')
	t.insert(rowkey,
		{
		'read':'ACGT
		})
	print 'insert finished '
	
stargate()
