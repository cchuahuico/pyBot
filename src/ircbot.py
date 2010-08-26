#!/usr/bin/env python

"""
   ircbot.py

   Handles all the protocols and factories. This is where the behavior of the bot is 
   defined and it is where the bot is connected.

"""

from sys import stdout
from twisted.python.log import startLogging
from twisted.internet import reactor, protocol
from twisted.words.protocols import irc
import datacollect
from botconfig import BotConfig

config = BotConfig()

class IRCProtocol(irc.IRCClient):
    nickname = config.get_nick().encode("ascii")

    def signedOn(self):
        # Identify myself to NickServ so I can join
        # +r (must be registered) channels
        self.msg("NickServ", "identify " + config.get_pass().encode("ascii"))

    def privmsg(self, user, channel, message):
        # This method logs ALL messages by users in channel

        username = self.extract_nick(user)

        # have the data collector instance parse the message
        self.factory.parse_message(username, channel, message)

        # join channel immediately after being identified by NickServ
        if "You are now identified" in message:
            self.join_channels()

    def join_channels(self):
        channels = map(lambda s: s.encode("ascii"), config.get_channels())
        for chan in channels:
            self.join(chan)

    def extract_nick(self, user):
        # format of original user param is nickname!~host
        # this line basically splits the format to (nickname, !, host) 
        # and grabs the nickname       
        return user.partition('!')[0]

    # disabled this method for now
    def userQuit(self, user, quitMessage):
        if self.extract_nick(user) == "":
            self.factory.stop_reactor()

class IRCFactory(protocol.ClientFactory):
    protocol = IRCProtocol

    def __init__(self):
        self.collector = datacollect.DataCollector()

    def clientConnectionFailed(self, connector, reason):
        print "Connection failed: %s" % reason
        self.stop_reactor()
    
    def stop_reactor(self):
        self.collector.close()
        reactor.stop()

    def parse_message(self, username, channel, message):
        self.collector.extract_links(username, channel, message)

if __name__ == "__main__":
    host, port = config.get_host(), int(config.get_port())

    # all output will be logged to reactor.log including errors and tracebacks
    startLogging(open(config.get_reactor_path(), "a"))
    reactor.connectTCP(host, port, IRCFactory())
    reactor.run()
