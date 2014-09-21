# -*- coding: utf-8 -*-
# :Progetto:  metapensiero.firefox_places -- tests
# :Creato:    ven 19 set 2014 19:06:29 CEST
# :Autore:    Alberto Berti <alberto@metapensiero.it>
# :Licenza:   GNU General Public License version 3 or later
#

import unittest
import metapensiero.firefox_places as ff

class BaseTestCase(unittest.TestCase):

    _file = 'places.sqlite'

    def _open_db_file(self, fname):
        import os
        fpath = os.path.join(os.path.dirname(__file__), fname)
        return ff.connect(fpath, echo=True)

    def setUp(self):
        self.e, self.s = self._open_db_file(self._file)
