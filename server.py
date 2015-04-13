#!/usr/bin/env python
#coding:utf-8

import tornado.ioloop
import tornado.options
import tornado.httpserver
import os 
import sys

from application import application

from tornado.options import define,options
define("port",default=8888,help="run on th given port",type=int)

class  IndexHandler(tornado.web.RequestHandler):
	def get(self):
	        lst = ["python","www.itdiffer.com","qiwsir@gmail.com"]
	        self.render("index.html", info=lst)

def main():
	tornado.options.parse_command_line()
	application = tornado.web.Application(
		handlers=[(r'/',IndexHandler)],
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
