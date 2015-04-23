from xml.etree import ElementTree
import os 
import sys 
from optparse import OptionParser
import string
from collections import deque
reload(sys)
sys.setdefaultencoding('utf-8')

def xmlparse():
	currentdir = os.getcwd()
	# file = currentdir + '/xmldata/DRA002064.experiment.xml'
	# file = '/home/tokyo/bishe/repo/xmldata/SRA069358.experiment.xml'

	root_dir = '/home/tokyo/bishe/repo/hbaseindexing/NCBI_SRA_Metadata_All_20140722/'
	tsv  = currentdir+ '/SRA.tsv'
	outputFile = open(tsv, "w+")
	row_counter =0 



	for subdir in os.listdir(root_dir):
		run_flag = 0 
		sample_flag = 0 
		experiment_flag = 0 
		# subdir = "SRA175322"

		for files in os.listdir(os.path.join(root_dir,subdir)):
			if  files.split('.')[1] == 'experiment':
				experiment_flag = 1 
				experiment_file  =  os.path.join(root_dir+subdir,files)
			if files.split('.')[1] == 'run':
				run_flag = 1
				run_file =  os.path.join(root_dir+subdir,files)
			if  files.split('.')[1] == 'sample':
				sample_flag = 1 
				sample_files =  os.path.join(root_dir+subdir,files)
		# flag  1  experient ;2 run; 3 sample 
 		if experiment_flag == 0 :
			continue 

		# for files in os.listdir(os.path.join(root_dir,subdir)):
		# 	file = os.path.join(root_dir+subdir,files)
		run_queue = deque('')
		sample_queue = deque('')
		# # tsv = options.tsvname	https://github.com/uprush/hac-book/blob/master/2-data-migration/script/to_tsv_hly.
		if run_flag == 1 and experiment_flag ==1 :
			file = run_file
			with open(file, 'rt') as f:
		    		tree = ElementTree.parse(f)
		    		root = tree.getroot()
				for node in tree.iter():
					if node.tag  == 'RUN':
						run_queue.append(node.get("accession"))
						print node.get("accession")
		if sample_flag == 1 and  experiment_flag == 1 :
			file = sample_files 
			with open(file, 'rt') as f:
		    		tree = ElementTree.parse(f)
		    		root = tree.getroot()
				for node in tree.iter():
					if node.tag  == 'EXTERNAL_ID':
						if  node.get('namespace') == 'BioSample':
							sample_queue.append(node.text)
		if experiment_flag == 1:
			file = experiment_file
			with open(file, 'rt') as f:
		    		tree = ElementTree.parse(f)
		    		root = tree.getroot()
		    		value_list = ['0' for i in range(0,11)]
				datas = ['0' for i in range(0,13)]	

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
			   		if node.tag == 'TITLE' :
			   			value_list[2]= node.text
			   			print node.text
			   		if  node.tag == 'DESIGN_DESCRIPTION':
			   			value_list[3] = node.text
			   			print node.text 
			   		if node.tag == 'STUDY_REF':
			   			value_list[4] =node.get('accession')
			   			print node.get('accession')
			   		if node.tag == 'EXTERNAL_ID':
			   			if node.get('namespace') == 'BioProject' :
			   				print 'BioProject    '+node.text
			   				value_list[5] = node.text
			   		# for item in root.iter('STUDY_REF'):
			   		# 	print item 
			   		if node.tag  == 'LIBRARY_DESCRIPTOR':
			   			if node.find('LIBRARY_NAME') != None:
			   				value_list[6] = node.find('LIBRARY_NAME').text	
			   			value_list[7]=node.find('LIBRARY_STRATEGY').text
			   			value_list[8]=node.find('LIBRARY_SOURCE').text
			   			value_list[9]= node.find('LIBRARY_SELECTION').text
			   			print node.find('LIBRARY_STRATEGY').text
			   			print node.find('LIBRARY_SOURCE').text
			   			print node.find('LIBRARY_SELECTION').text
			   		if node.tag == 'INSTRUMENT_MODEL':
			   			value_list[10]=node.text 
			   			print node.text #IRON Torrent PGM
						datas = ['0' for i in range(0,13)]	
					   	datas[1:11]= value_list
					   	datas[0] = 'row'+str(row_counter)
					   	row_counter = row_counter+1
					   	if  run_flag==1  :# run exist
					   		if len(run_queue) > 0:
					   			datas[12]  = run_queue.popleft()
					   	if sample_flag == 1:  #sample file exist 
					   		if  len(sample_queue) > 0:
					   			datas[13] = sample_queue.popleft()
					   	for i in range(1,13):
					   		if datas[i] == None:
					   			 datas[i]  = ''
						print datas
						outputFile.write(string.join(datas, "\t") + "\n")

		# break
	outputFile.close()

# 	two way of getting value:
	# for node in  tree.ite():  node.tag == ; then node.get('atttrib_name') or node.find('child').text
	# for item in root.ite('tag') ; item.attrib['attrib_name'] or item.text

	   			

xmlparse()

