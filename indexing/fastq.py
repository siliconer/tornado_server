import os 
import string
def extract_fastq():
	current_dir =os.getcwd()
	fastq_file_one =  current_dir + '/fastq/SRR1514737_1.fastq'
	fastq_file_two = current_dir + '/fastq/SRR1514737_2.fastq'
	tsv  = current_dir+ '/SRA_fastq.tsv'
	outputFile = open(tsv, "a")

	row_number = 1300000
	data =[[ 0 for i in range(0,2)] for j in range(0,row_number) ]
	read_fastq(fastq_file_one,1,outputFile)
	read_fastq(fastq_file_two,2,outputFile)

def read_fastq(file,file_index,outputFile):
	reader = open(file, "rb")
	title=""
	buffer=""
	bio_read_exist = 0 
	index = 0 
	data = [0 for i in range(0,3)]
	while 1:
		line = reader.readline()
		if line == "":
		    break
		if bio_read_exist == 1:
			# print ' bio_read ' +line
			data[2] = str(line.replace('\n', ' ').replace('\r', '')) 
			index = index + 1 
			bio_read_exist = 0 
			outputFile.write(string.join(data, "\t") + "\n")

		if line.startswith("@"):
			id =   line.split(' ')[0][1:]
			data[0]=str(index) 
			if id.startswith("S"):
				data[1] = id+'.'+str(file_index)
				print data[0]
				bio_read_exist = 1

extract_fastq()


