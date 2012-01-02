Aleph Python API
================

Usage
-----

The `aleph` module offers a single class named `Aleph`, which wraps the functionality of the Aleph web interface. Currently, this includes login/logout and getting the list of loaned books. For further information, see the example below.

	>>> from aleph import Aleph
	>>> a = Aleph()
	>>> a.login('http://aleph.omikk.bme.hu', 'username', 'password')
	>>> a.get_loaned()
	[{'title': u'Platon \xf6sszes m\u0171vei', 'due': datetime.datetime(2012, 2, 1, 20, 0), 'author': 'Platon'}, ...]
	>>> a.logout()

License
-------

The whole project is licensed under MIT license.

Dependencies
------------

 - Python 2.x (tested on 2.7)
 - LXML (Debian/Ubuntu package: `python-lxml`)
