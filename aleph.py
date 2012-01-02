#!/usr/bin/env python

from datetime import datetime
from urllib2 import urlopen
from urllib import urlencode
from random import randint
from lxml import etree
import re

LOANED_XPATH = '/html/body/table[@cellspacing=2]/tr[not(@class="tr1")]'
LOGIN_XPATH = '//a[contains(@href, "login-session")]/@href'
LIBRARY_XPATH = '//input[@name="bor_library"]/@value'
DUE_FORMAT = '%Y%m%d%H:%M'
SESSION_RE = re.compile(r"/F/([^?]+)?")
PARSER = etree.HTMLParser()

class Aleph(object):
    def __init__(self):
        self.session_id = None
        self.logged_in = False
        self.library = None
        self.url = None

    def login(self, url, username, password):
        self.url = url
        self.session_id = get_session_id(url)
        loginpage = self.get_parsed(func='login-session')
        (self.library,) = loginpage.xpath(LIBRARY_XPATH)
        login = urlopen('{0}/F/{1}'.format(url, self.session_id), urlencode({
            'func': 'login-session', 'bor_id': username,
            'bor_verification': password, 'bor_library': self.library}))
        if 'login-session' in login.read():
            raise RuntimeError('Authentication failure')
        self.logged_in = True

    def logout(self):
        self.get_parsed(func='logout')
        self.logged_in = False

    def get_loaned(self):
        if not self.logged_in:
            raise RuntimeError('Use login() first')
        tree = self.get_parsed(func='bor-loan', adm_library=self.library)
        loaned = tree.xpath(LOANED_XPATH)
        return map(convert_loan, loaned)

    def get_parsed(self, **kwargs):
        page = urlopen('{0}/F/{1}?{2}'.format(
            self.url, self.session_id, urlencode(kwargs)))
        return etree.parse(page, PARSER)


def get_session_id(url):
    rnd = randint(1, 1000000000)
    home = etree.parse(urlopen('{0}/F?RN={1}'.format(url, rnd)), PARSER)
    (loginlink,) = home.xpath(LOGIN_XPATH)
    return SESSION_RE.search(loginlink).group(1)

def convert_loan(loan):
    fields = loan.xpath('td')
    return {'author': fields[2].text, 'title': fields[3].text,
            'due': datetime.strptime(
                fields[5].text + fields[6].text, DUE_FORMAT)}
