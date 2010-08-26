"""
    datacollect.py

    This class handles collecting and filtering data (messages) it receives.
"""

import re
import urllib
from datetime import datetime
import codecs
import sys
from botconfig import BotConfig
from BeautifulSoup import BeautifulSoup

class DataCollector():

    def __init__(self):
        self.config = BotConfig()
        try:
            # Opening the links file with utf encoding is required because unicode data
            # has to be written to the file at times -- specifically the em character (\u2014)
            # which represents an underscore in the username
            self.link_log = codecs.open(self.config.get_link_path(), "a", encoding="utf-8")
            self.link_log.write(self.get_date() + "\n")
        except IOError:
            "links log can't be opened."

        # matches all valid urls but not ie. google.com
        # taken from regexlib.com
        self.pattern = """(((http|ftp|https|ftps|sftp)://)|(www\.))+(([a-zA-Z
                          0-9\._-]+\.[a-zA-Z]{2,6})|([0-9]{1,3}\.[0-9]{1,3}\.
                          [0-9]{1,3}\.[0-9]{1,3}))(/[a-zA-Z0-9\&amp;%_\./-~-]*)?"""

        # pattern used to filter links
        # keywords included in this pattern will NOT be included in the links log
        self.filter_pat = "(codepad|pastebin|pocoo)"

    def extract_links(self, user, chan, msg):
        # extracts all urls found in message and store in an iterator
        matches = re.finditer(self.pattern, msg.strip(), re.IGNORECASE + re.VERBOSE)
        for link in matches:
            # link.group() contains the full valid url extracted by the regex
            link = link.group()
            if not re.search(self.filter_pat, link, re.IGNORECASE) and not user == "ChanServ":
                title = self.get_title(link)
                self.link_log.write("%s - %s: %s > %s\n" % (chan, user, link, title))
                self.link_log.flush()

    def close(self):
        self.link_log.close()

    def get_date(self):
        # Return date in format: Sunday, August 01, 2010
        return datetime.now().strftime("%A, %B %d, %Y")

    def get_title(self, url):
        # Get contents of <title> tag in the url
        try:
            source = urllib.urlopen(url).read()
            return BeautifulSoup(source).title.text
        except:
            return "No Title"

