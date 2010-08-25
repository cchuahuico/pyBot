#!/usr/bin/env python

from sys import stdout
from twisted.python.log import startLogging
from twisted.internet import reactor, protocol
from twisted.words.protocols import irc
import datacollect

REACTOR_PATH = "/home/clarence/Projects/Python/IRCBot/data/reactor.log"

class IRCProtocol(irc.IRCClient):
    nickname = "Bobdroid"

    def signedOn(self):
        # Identify myself to NickServ so I can join
        # +r (must be registered) channels
        self.msg("NickServ", "identify bolenjx")

    def privmsg(self, user, channel, message):
        """This method logs ALL messages by users in channel"""

        username = self.extract_nick(user)

        # have the data collector instance parse the message
        self.factory.parse_message(username, channel, message)

        # join channel immediately after being identified by NickServ
        if "You are now identified" in message:
            self.join_channels()

    def join_channels(self):
        for chan in ["#python", "#java", "#c", "#c++", "#ubuntu"]:
            self.join(chan)

    def extract_nick(self, user):
        # format of original user param is nickname!~host
        # this line basically splits the format to (nickname, !, host) 
        # and grabs the nickname       
        return user.partition('!')[0]

    def userQuit(self, user, quitMessage):
        if self.extract_nick(user) == "CodingDistrict":
            print "CodingDistrict left freenode"
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
    host, port = "irc.freenode.net", 6667

    # all output will be logged to reactor.log including errors and tracebacks
    startLogging(open(REACTOR_PATH, "a"))
    reactor.connectTCP(host, port, IRCFactory())
    reactor.run()
