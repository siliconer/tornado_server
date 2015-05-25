import json
import base64
import requests
import os
import os.path	
from commands import *

from starbase import Connection 

def table_length(tablename,column_name):
	count_cmd = '/usr/bin/hbase org.apache.hadoop.hbase.mapreduce.RowCounter '+tablename +' '+column_name
	text = getoutput(count_cmd)
	index = text.find('ROWS')
	start_index= index
 	while(text[index] != '\n') :
		index = index + 1
	
	row_num =  text[start_index:index]	
	print row_num	
	added_row_num = row_num.split('=')[1]
	return added_row_num 

def  stargate(tablename,column_name,insert_data,added_row_num):
	c = Connection()
	c = Connection(host='127.0.0.1', port=7060)
	print	c.tables()
#	request = requests.get(baseurl + "/" + tablename + "/schema")
#	tablename = 'SRAtest'
#	column_name = 'EXPERIMENT_ID:
#	count_cmd = 'ls '
	print added_row_num
#	added_row_num =  64043
	row_key =  'row' +str(added_row_num)
	t = c.table(tablename)
 	print row_key	
#	t.insert(rowkey,
#		{
#		'read':'ACGT'}
#		)
	if  column_name.find(':') == -1:
		t.insert(row_key,
			{
			column_name:
				{ '':insert_data}
			}
			)
	else:
		column = column_name.split(':')[0]
		key = column_name.split(':')[1]
		t.insert(row_key,
			{
			column:
				{ key:insert_data}
			}
			)
	print 'insert finished '
	print t.fetch(row_key,[column_name])
#	print t.fetch('SRR1514737.1600002.1',['read'])
	
#stargate(tablename.column_name,insert_data)
