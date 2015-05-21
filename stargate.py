from common import *
import json
import base64
import requests
def issuccessful(request):
	if 200 <= request.status_code and request.status_code <= 299:
		return True
	else:
		return False
def parse_stargate(query_str):
	tablename = 'SRR1514737'
	# query_row_key = 'SRR1514737.1757.1'
	query_row_key_one = query_str + '.1'
	query_row_key_two = query_str+  '.2'
	read_one = query(query_row_key_two)
	read_two = query(query_row_key_one)
	return read_one,read_two 
def query(query_row_key):
	column_name = 'read'
	baseurl =  'http://localhost:7060'
	request = requests.get(baseurl + "/" + tablename +"/"+query_row_key+'/'+ column_name, headers={"Accept" : "application/json"})

	if issuccessful(request) == False:
		print "Could not get messages from HBase. Text was:\n" + request.text
		quit()

	bleats = json.loads(request.text)

	# bleats= '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><CellSet><Row key="U1JSMTUxNDczNy4xNzU3LjE=">
	# <Cell column="cmVhZDo=" timestamp="1432216066594">Q0FHR1RHQ1RBQUdDR1RBQUdUR0NBQUFBVEdDQ0FHVEdUQ0dHVEdBQUF
	# UR0FDR0NDVENDVENHQ1RDQUNUQ0dHVENHQ1RBQ0dDVENDVEdDQ0dUR0FHQUNUR0NHR0NHR0dDR1RUQUNHR0dDVFRBQ0FHQV
	# RBQUNHQUdBR0FHQ0FHQVRHR0FHQUdBQUdUQ0FHR0dBR0FHQ1RHQ0dBQUFBR0dBVEdDR0dDR1RUR0NDR1RUVFRUQ0NBVEFHR0N
	# UQ0NHQ0NDQ0NDVEdBQ0FBR0NBVENBQ0dBQUFUQ1RHQUNHQ1RDQUFBVENBR1RHR1RHR0NHQUFBQ0NDR0FDQUdHIA==</Cell></Row></CellSet>'
	for row in bleats['Row']:
		message = ''
		lineNumber = 0
		username = ''
		print 'row'
		print row 
		for cell in row['Cell']:
			columnname = base64.b64decode(cell['column'])
			value = cell['$']
			
			if value == None:
				continue


		rowKey = base64.b64decode(row['key'])
	return base64.b64decode(value)

