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
    column_property
)

from sqlalchemy.sql import (
    case,
    and_,
    bindparam
)

from sqlalchemy.ext.declarative import (
    declared_attr
)

from . import Base, UTCTimestamp

logger = logging.getLogger(__name__)


class StructureItem(Base):
    """
    sqlite> .schema moz_bookmarks
    CREATE TABLE moz_bookmarks (
       id INTEGER PRIMARY KEY,
       type INTEGER,
       fk INTEGER DEFAULT NULL,
       parent INTEGER,
       position INTEGER,
       title LONGVARCHAR,
       keyword_id INTEGER,
       folder_type TEXT,
       dateAdded INTEGER,
       lastModified INTEGER,
       guid TEXT);
    CREATE INDEX moz_bookmarks_itemindex ON moz_bookmarks (fk, type);
    CREATE INDEX moz_bookmarks_parentindex ON moz_bookmarks (parent, position);
    CREATE INDEX moz_bookmarks_itemlastmodifiedindex ON moz_bookmarks (fk, lastModified);
    CREATE UNIQUE INDEX moz_bookmarks_guid_uniqueindex ON moz_bookmarks (guid);

    # const short TYPE_BOOKMARK = 1;
    # const short TYPE_FOLDER = 2;
    # const short TYPE_SEPARATOR = 3;
    """
    __tablename__ = 'moz_bookmarks'

    id = Column('id', Integer, primary_key=True)
    type = Column('type', Integer)
    fk = Column('fk', Integer, ForeignKey('moz_places.id'))
    idparent = Column('parent', Integer, ForeignKey('moz_bookmarks.id'))

    parent = relationship('StructureItem', backref=backref('children'),
                          remote_side='StructureItem.id')

    date_added = Column('dateAdded', UTCTimestamp)
    date_last_modify = Column('lastModified', UTCTimestamp)

    _places_p = bindparam('places_id', callable_=lambda: Base._roots.get('places', 1))
    _menu_p = bindparam('menu_id', callable_=lambda: Base._roots.get('menu', 2))
    _toolbar_p = bindparam('toolbar_id', callable_=lambda: Base._roots.get('toolbar', 3))
    _tags_p = bindparam('tags_id', callable_=lambda: Base._roots.get('tags', 4))
    _unfiled_p = bindparam('unfiled_id', callable_=lambda: Base._roots.get('unfiled', 5))

    __mapper_args__ = {'polymorphic_on': case([
            (type == 1, 'bookmark'),
            (type == 3, 'separator'),
            (and_(type == 2,
                  idparent == _tags_p), 'tag'),
            (and_(type == 2,
                  id == _places_p), 'places'),
            (and_(type == 2,
                  id == _menu_p), 'menu'),
            (and_(type == 2,
                  id == _toolbar_p), 'toolbar'),
            (and_(type == 2,
                  id == _tags_p), 'tags'),
            (and_(type == 2,
                  id == _unfiled_p), 'unfiled'),
            (type == 2, 'folder'),
    ])}

    del _places_p, _menu_p, _toolbar_p, _tags_p, _unfiled_p

class Bookmark(StructureItem):

    place = relationship('Place', backref=backref('bookmarks'))
    __mapper_args__ = {'polymorphic_identity': 'bookmark'}

class Separator(StructureItem):

    __mapper_args__ = {'polymorphic_identity': 'separator'}

class Folder(StructureItem):

    __mapper_args__ = {'polymorphic_identity': 'folder'}

class Tag(Folder):

    __mapper_args__ = {'polymorphic_identity': 'tag'}

class Tags(Folder):

    __mapper_args__ = {'polymorphic_identity': 'tags'}

class Unfiled(Folder):

    __mapper_args__ = {'polymorphic_identity': 'unfiled'}

class Places(Folder):

    __mapper_args__ = {'polymorphic_identity': 'places'}

class Menu(Folder):

    __mapper_args__ = {'polymorphic_identity': 'menu'}

class Toolbar(Folder):

    __mapper_args__ = {'polymorphic_identity': 'toolbar'}
