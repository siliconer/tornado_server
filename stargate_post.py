import json
import base64
import requests
import os
import os.path	
from commands import *

from starbase import Connection 

def  stargate(tablename,column_name,insert_data):
	c = Connection()
	c = Connection(host='127.0.0.1', port=7060)
	print	c.tables()
#	request = requests.get(baseurl + "/" + tablename + "/schema")
#	tablename = 'SRAtest'
#	column_name = 'EXPERIMENT_ID:
	count_cmd = '/usr/bin/hbase org.apache.hadoop.hbase.mapreduce.RowCounter '+tablename +' '+column_name
#	count_cmd = 'ls '
	text = getoutput(count_cmd)
	print text
	index = text.find('ROWS')
	start_index= index
 	while(text[index] != '\n') :
		index = index + 1
	
	row_num =  text[start_index:index]	
	print row_num	
	added_row_num = row_num.split('=')[1]
#	rowkey = 'SRR1514737.1600002.1'
	print added_row_num
#	added_row_num =  64043
	row_key =  'row' +str(added_row_num)
	t = c.table(tablename)
 	print row_key	
#	t.insert(rowkey,
#		{
#		'read':'ACGT'}
#		)

	t.insert(row_key,
		{
		column_name:
			{ '':insert_data}
		}
		)

	print 'insert finished '
	print t.fetch(row_key,[column_name])
#	print t.fetch('SRR1514737.1600002.1',['read'])
	
#stargate(tablename.column_name,insert_data)
