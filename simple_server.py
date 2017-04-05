#!/usr/bin/env python

# Copyright 2017 Lev Meirovitch
# This is Free Software distirbuted under the MIT license
# See COPYING or https://opensource.org/licenses/MIT for details

from BaseHTTPServer import HTTPServer
from BaseHTTPServer import BaseHTTPRequestHandler
from urllib import unquote

""" This class does all the work
	Just overwrite the function for the HTTP method you want to handle and
	put your code there.
	The base class handles everything else: sending response codes and headers,
	providing input stream for POST parameters and output stream for response
	content, and even some basic parsing of request headers.
"""
class HttpPartsHandler(BaseHTTPRequestHandler):
	# this will get called for every GET request, just add your code here
	def do_GET(self):
		# use some convenience functions to comply with HTTP protocol 
		self.send_ok_reply()

		# do some basic string operations
		path, query = self.initial_split()
		parts = self.split_path(path)
		args = self.split_query(query)
		
		# write some HTML text
		self.print_head()
		self.pritty_print_path(parts)
		self.pritty_print_args(args)
		self.print_tail()
		
		# all done!


	""" Base class treats path and query parameters both as 'path'
	    This funtion will split them for separate handling

	    @return tupel of strings (path, query)
	"""
	def initial_split(self):
		if '?' in self.path:
			as_list = self.path.split('?', 1)
			return (as_list[0], as_list[1])

		return (self.path, None)


	""" Splits the query string in to list of dictionaries with

		@param query string to parse
		@return list of form: [ { name : param_name, value : param_value } ] or
			None if empty string is given
	"""
	def split_query(self, query):
		if query is None:
			return None

		couples = query.split('&')
		params = []

		for couple in couples:
			as_list = couple.split('=')

			params.append({ 'name' : as_list[0],
				'value' : as_list[1] if len(as_list) > 1 else None })

		return params


	""" Split path to list of components

		@return path components as list, or None if no path (root)
	"""
	def split_path(self, path):
		if path is None or len(path) < 2:
			return None

		parts = path.split('/')
		if len(parts) < 2 or len(parts[1]) < 1:
			return None

		return parts[1:]


	""" Prints path components in formatted HTML list

		@param parts list of 0 or more strings
	"""
	def pritty_print_path(self, parts):
		try:
			if parts is not None:
				self.wfile.write("<br/>Path components:<br/>\n")
				self.wfile.write("<ol>\n")

				for part in parts:
					self.wfile.write("<li>")
					self.wfile.write(part)
					self.wfile.write("</li>\n")

				self.wfile.write("</ol>\n")
			else:
				self.wfile.write("<br/><strong>Path is empty.</strong><br/>\n")

		except IOError:
			print "Error writing response body."


	""" Prints query parameters and their values as formatted HTML list

		@param list of 0 or more name-value dictinaries
	"""
	def pritty_print_args(self, args):
		try:
			if args is not None:
				self.wfile.write("<br/>Query parameters:<br/>\n")
				self.wfile.write("<ul>\n")

				for arg in args:
					self.wfile.write("<li>")
					self.wfile.write(arg['name'])
					self.wfile.write(' = ')
					if arg['value'] is not None:
						self.wfile.write(unquote(arg['value']))
					self.wfile.write("</li>\n")

				self.wfile.write("</ul>\n")
			else:
				self.wfile.write("<br/><strong>No query in URL.</strong><br/>\n")

		except IOError:
			print "Error writing response body."


	# minimal header for correct HTML response
	def send_ok_reply(self):
		self.send_response(200)
		
		# these are only needed if you want to display HTML in browser
		# you can skip them for custom client software
		self.send_header('Content-Type', 'text/html; charset=UTF-8')
		self.end_headers()


	# opening HTML boilerplate
	def print_head(self):
		try:
			self.wfile.write("<!DOCTYPE html>\n<head>\n")
			self.wfile.write("<title>HTTP Everywhere!</title>\n")
			self.wfile.write("</head>\n<body>")
		except IOError:
			print "Error writing response head."


	# closeing HTML boilerplate
	def print_tail(self):
		try:
			self.wfile.write("</body>")
		except IOError:
			print "Error writing response tail."

# this is the server setup:
# just two lines!
server = HTTPServer(('', 8080), HttpPartsHandler) # create server instance
try:
	server.serve_forever() # handle requests
except KeyboardInterrupt: # this is just to avoid ugly stack trace on exit
	print "Shutting down server"
	exit(0)
