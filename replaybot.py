#!/usr/bin/python

#This is a bot that will recieve a message at a URL via POST and say it in
# an XMPP MUC. Do the simplest thing that could work, right?

from twisted.words.protocols.jabber import client, jid #Jabber client
from twisted.words.xish import domish, xmlstream
from twisted.web.server import Site #Web server for POST requests
from twisted.web.resource import Resource
from twisted.internet import reactor, defer #And, of course, the reactor

from sys import stdout
from twisted.python.log import startLogging; startLogging(stdout)


#Get POST requests
class WebServer(Resource):
	def __init__(self, jabberClient):
		self.jabberClient = jabberClient

	def render_POST(self, request):
		"""Respond to a POST request"""
		print request.args["message"][0]
		self.jabberClient.sendMessage(request.args["message"][0])
		return ''

class JabberClient():
	def __init__(self):
		self.jid = 'robot@ais/twisted'
		self.password = 'password'
		self.server = 'ais'
		self.port = 5222
		self.room = 'support@chat.ais'
		self.nickname = 'PaulRevere'
		self.xmlstream = ''

	def authFailed(self, xmlstream):
		"""Authentication failed"""
		global reactor
		print 'authentication failed'
		reactor.stop()

	def authd(self, xmlstream):
		"""Authenticate with the server"""
		print "authenticated"
		
		presence = domish.Element(('jabber:client', 'presence'))
		presence.addElement('status').addContent('Online')
		xmlstream.send(presence)

		#xmlstream.addObserver('/message', self.debug)
		#xmlstream.addObserver('/presence', self.debug)
		#xmlstream.addObserver('twisted.words.xish.xmlstream.STREAM_ERROR_EVENT', self.debug)
		self.xmlstream = xmlstream
		self.joinRoom(xmlstream)

	def joinRoom(self, xmlstream):
		"""Join a MUC"""
		#We don't want to recieve any history upon entering the room
		history = domish.Element((None, 'history'))
		history['maxchars'] = '0'
		
		#We're using Multi-User Chat
		x = domish.Element((None, 'x'))
		x['xmlns'] = 'http://jabber.org/protocol/muc'
		
		#And we're sending it to this chat room
		presence = domish.Element((None, 'presence'))
		presence['from'] =  self.jid
		presence['to'] = self.room + '/' + self.nickname
		
		x.addChild(history)
		presence.addChild(x)
		print presence.toXml()
		xmlstream.send(presence)

	def sendMessage(self, message):
		"""Send a message to the MUC"""
		m = domish.Element((None, 'message'))
		m['from'] = self.jid
		m['to'] = self.room
		m['type'] = 'groupchat'
		m.addElement('body', content = message)
		self.xmlstream.send(m)

	def debug(self, element):
		print element.toXml().encode('utf-8')
		print '='*20

#Jabber setup
jabberClient = JabberClient()
jabberFactory = client.basicClientFactory(jid.JID(jabberClient.jid), jabberClient.password)
jabberFactory.addBootstrap('//event/stream/authd', jabberClient.authd)
jabberFactory.addBootstrap('//event/client/basicauth/authfailed', jabberClient.debug)
reactor.connectTCP(jabberClient.server, jabberClient.port, jabberFactory)

#Webserver setup
serverRoot = Resource()
serverRoot.putChild("robot", WebServer(jabberClient))
webFactory = Site(serverRoot)
reactor.listenTCP(8880, webFactory)

reactor.run() #Into the hands of fate!
