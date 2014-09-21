# -*- coding: utf-8 -*-
# :Progetto:  metapensiero.firefox_places -- moz_places model
# :Creato:    mar 16 set 2014 14:20:43 CEST
# :Autore:    Alberto Berti <alberto@metapensiero.it>
# :Licenza:   GNU General Public License version 3 or later
#

import logging

from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime
    )

from sqlalchemy.orm import (
    relationship,
    backref,
    deferred,
)

from . import Base, UTCTimestamp

logger = logging.getLogger(__name__)


class Place(Base):
    """
    sqlite> .schema moz_places
    CREATE TABLE moz_places (
       id INTEGER PRIMARY KEY,
       url LONGVARCHAR,
       title LONGVARCHAR,
       rev_host LONGVARCHAR,
       visit_count INTEGER DEFAULT 0,
       hidden INTEGER DEFAULT 0 NOT NULL,
       typed INTEGER DEFAULT 0 NOT NULL,
       favicon_id INTEGER,
       frecency INTEGER DEFAULT -1 NOT NULL,
       last_visit_date INTEGER ,
       guid TEXT,
       foreign_count INTEGER DEFAULT 0 NOT NULL);
    CREATE INDEX moz_places_faviconindex ON moz_places (favicon_id);
    CREATE INDEX moz_places_hostindex ON moz_places (rev_host);
    CREATE INDEX moz_places_visitcount ON moz_places (visit_count);
    CREATE INDEX moz_places_frecencyindex ON moz_places (frecency);
    CREATE INDEX moz_places_lastvisitdateindex ON moz_places (last_visit_date);
    CREATE UNIQUE INDEX moz_places_url_uniqueindex ON moz_places (url);
    CREATE UNIQUE INDEX moz_places_guid_uniqueindex ON moz_places (guid);
    """

    __tablename__ = 'moz_places'
    last_visit_date = Column('last_visit_date', UTCTimestamp , nullable=False)
