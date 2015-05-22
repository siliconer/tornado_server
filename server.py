#!/usr/bin/env python
#coding:utf-8

import tornado.ioloop
import tornado.options
import tornado.httpserver
import os 
import sys
import json
from application import application
from urllib2 import *
import simplejson
from stargate import parse_stargate
from tornado.options import define,options
define("port",default=8888,help="run on th given port",type=int)

class  IndexHandler(tornado.web.RequestHandler):
	def get(self):
		print '/'
		self.render("bootstrap_intro.html")
	def write_error(self, status_code, **kwargs):
      		  self.write("IndexHandler darnit, user! You caused a %d error." % status_code)
class  SearchHandler(tornado.web.RequestHandler):
	def  post(self):
		searchterm = self.get_argument('searchterm')
		query_url  = ' http://192.168.0.108:8983/solr/sra_collection_shard1_replica1/select?q=*' + searchterm + '*&rows=100000&wt=json'
		print query_url + ' search'	
		response = simplejson.load(urlopen(query_url))
		print response
		out_file = os.getcwd() + '/static/search.json'
		with open(out_file,"w") as outfile:
			json.dump(response,outfile,indent=4)
		#file = open(out_file,"w")
       		#file.write(str(response))
		# print reponse
		#file.close()
		self.render('search.html',json='/static/search.json')
		#self.render('search.html')	
	def write_error(self, status_code, **kwargs):
       		 self.write("SearchHandler darnit, user! You caused a %d error." % status_code)
class WrappHandler(tornado.web.RequestHandler):
	def post(self):
		text = self.get_argument('text')
		self.write(text)
class  IdHandler(tornado.web.RequestHandler):
	def get(self,input_word):
		print input_word
		# json_file = os.getcwd()+'/static/ERX081395.json'
		# json_body = json.load(open(json_file))['response']['docs'][0]
		query_url  = ' http://192.168.0.108:8983/solr/sra_collection_shard1_replica1/select?q=*'+ input_word+ '*&wt=json'
		print query_url	
		response = simplejson.load(urlopen(query_url))
		json_body = response['response']['docs'][0]
		experiment_id=json_body['experiment_id']
		title = json_body['title']
		sample_id = json_body['experiment_id']
		library_selection = json_body['library_selection']
		design_description = json_body['design_description']
		study_bioproject_id = json_body['study_bioproject_id']
		library_name = json_body['library_name']
		library_source= json_body['library_source']
		library_strategy = json_body['library_strategy']
		run_id = json_body['run_id']
		submitter_id = json_body['submitter_id']
		instrument_model = json_body['instrument_model']
		study_ref = json_body['study_ref']
		self.render("id.html",library_selection=library_selection,experiment_id=experiment_id,sample_id=sample_id,design_description=design_description,study_bioproject_id=study_bioproject_id,library_name=library_name,library_source=library_source,title=title,library_strategy=library_strategy,run_id=run_id,submitter_id=submitter_id,instrument_model=instrument_model,study_ref=study_ref)

		# http://192.168.0.108:8983/solr/sra_collection_shard1_replica1/select?q=*ERX081395*&wt=json&indent=true

class  SRRRunHandler(tornado.web.RequestHandler):
	def post(self):
		print 'srr'
		print str(self.request.body)+' a'
#		input_word=self.get_argument('td')
		input_word = tornado.escape.json_decode(self.request.body)
		print input_word
		read_info  = parse_stargate(str(input_word))
		#self.write('read_info')
		self.write({'read_info':read_info})
		self.flush()
		self.finish()

		print read_info
#	def get(self,input_word):
#		print 'get'
#		print self.request
#		print input_word[1:]
		#read_info = parse_stargate(input_word[1:])
		#print read_info
		
		
class RunHandler(tornado.web.RequestHandler):
	def get(self,input_word):
		print 'run'
		self.render('run.html',run_id =  SRR1514737,run_count = 120)

def main():
	tornado.options.parse_command_line()
	application = tornado.web.Application(
		handlers=[(r'/',IndexHandler),
		(r'/search',SearchHandler),
		(r'/wrap',WrappHandler),
		(r'/id/(\w+)',IdHandler),
		(r'/srun',SRRRunHandler),
		(r'/srun/(\w+)',SRRRunHandler),
		(r'/run/(\w+)',RunHandler)] ,
   	    	template_path=os.path.join(os.path.dirname(__file__),"template"),
  	    	static_path=os.path.join(os.path.dirname(__file__),"static"),	
  	    	debug = True
  	 )
	http_server = tornado.httpserver.HTTPServer(application)
	http_server.listen(options.port)
	print 'Development server is running at http://127.0.0.1:%s/' % options.port
	print 'Quit the server with Contro'
	tornado.ioloop.IOLoop.instance().start()

	# tornado.ioloop.IOLoop.instance().start()

main()
