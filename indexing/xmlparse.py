from xml.etree import ElementTree
import os 
import sys 
from optparse import OptionParser
import string
reload(sys)
sys.setdefaultencoding('utf-8')

def xmlparse():
	currentdir = os.getcwd()
	# file = currentdir + '/xmldata/DRA002064.experiment.xml'
	# file = '/home/tokyo/bishe/repo/xmldata/SRA069358.experiment.xml'

	root_dir = '/home/tokyo/bishe/repo/hbaseindexing/xmldata/'
	tsv  = currentdir+ '/SRA.tsv'
	outputFile = open(tsv, "w+")
	row_counter =0 

	for files in os.listdir(root_dir):
		file = os.path.join(root_dir,files)
		print file
		# file ='/home/tokyo/bishe/repo/hbaseindexing/xmldata/SRA091447.experiment.xml'
		value_list = ['0' for i in range(0,8)]
		datas = ['0' for i in range(0,9)]		
		# filename = options.filename
		# tsv = options.tsvname	https://github.com/uprush/hac-book/blob/master/2-data-migration/script/to_tsv_hly.py

		with open(file, 'rt') as f:
	    		tree = ElementTree.parse(f)
	    		root = tree.getroot()

			# print tree
			# for item in root.iter('EXPERIMENT'):
			# 	print item.attrib['accession']	  #  DRX016088
			# 	value_list[0] = item.attrib['accession']	 
			for node in tree.iter():
				if node.tag == 'EXPERIMENT':
					value_list[0] = node.get('accession')
					experiment_counter = 1
		   		if  node.tag ==  'SUBMITTER_ID':
		   			value_list[1] = node.get('namespace')
		   			print node.get('namespace')
		   		if node.tag == 'TITLE':
		   			value_list[2]= node.text
		   			print node.text
		   		if node.tag == 'STUDY_REF':
		   			value_list[3] =node.get('accession')
		   			print node.get('accession')
		   		if node.tag  == 'LIBRARY_DESCRIPTOR':
		   			value_list[4]=node.find('LIBRARY_STRATEGY').text
		   			value_list[5]=node.find('LIBRARY_SOURCE').text
		   			value_list[6]= node.find('LIBRARY_SELECTION').text
		   			print node.find('LIBRARY_STRATEGY').text
		   			print node.find('LIBRARY_SOURCE').text
		   			print node.find('LIBRARY_SELECTION').text
		   		if node.tag == 'INSTRUMENT_MODEL':
		   			value_list[7]=node.text 
		   			print node.text #IRON Torrent PGM
				   	datas[1:9]= value_list
				   	datas[0] = 'row'+str(row_counter)
				   	row_counter = row_counter+1
				   	for i in range(1,9):
				   		if datas[i] == None:
				   			 datas[i]  = ''
				   	outputFile.write(string.join(datas, "\t") + "\n")
					print value_list
	outputFile.close()

# 	two way of getting value:
	# for node in  tree.ite():  node.tag == ; then node.get('atttrib_name') or node.find('child').text
	# for item in root.ite('tag') ; item.attrib['attrib_name'] or item.text

	   			

xmlparse()

