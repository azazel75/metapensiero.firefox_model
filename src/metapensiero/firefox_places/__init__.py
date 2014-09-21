# -*- coding: utf-8 -*-
# :Progetto:  metapensiero.firefox_places --
# :Creato:    mar 16 set 2014 14:32:32 CEST
# :Autore:    Alberto Berti <alberto@metapensiero.it>
# :Licenza:   GNU General Public License version 3 or later
#

from sqlalchemy import create_engine

from sqlalchemy.ext.declarative import (
    declarative_base,
    DeferredReflection)

from sqlalchemy.orm import (
    object_session,
    scoped_session,
    sessionmaker,
    )

class AbstractBase(object):
    "Abstract base entity class."

    def delete(self):
        "Delete this instance from the database."

        object_session(self).delete(self)

    def __repr__(self):
        "Return an ASCII representation of the entity."

        from sqlalchemy.orm.exc import DetachedInstanceError

        mapper = self.__mapper__
        pkeyf = mapper.primary_key
        try:
            pkeyv = mapper.primary_key_from_instance(self)
        except DetachedInstanceError:
            keys = u"detached-instance"
        else:
            keys = u', '.join(u'%s=%s' % (f.name, v)
                              for f, v in map(None, pkeyf, pkeyv))
        return u'<%s %s>' % (# pragma: no cover
                             self.__class__.__name__, keys)

DBSession = scoped_session(sessionmaker())
"The global SA session maker"

_Base = declarative_base(cls=AbstractBase)

class Base(DeferredReflection, _Base):
    "The common parent class for all declarative mapped classed."
    __abstract__ = True

    @classmethod
    def prepare(cls, engine):
        cls.resolve_roots(engine)
        super(cls, Base).prepare(engine)

    @classmethod
    def resolve_roots(cls, engine):
        from sqlalchemy import Table, select
        roots = Table('moz_bookmarks_roots',
                      cls.metadata,
                      extend_existing=True,
                      autoload_replace=False,
                      autoload=True,
                      autoload_with=engine)
        cls._roots = dict(list(engine.execute(select([roots.c.root_name,
                                                     roots.c.folder_id]))))

import datetime, time
from sqlalchemy.types import TypeDecorator, Integer

class UTCTimestamp(TypeDecorator):
    impl = Integer

    divider = 1000000.0

    epoch = datetime.datetime(1970, 1, 1, 0, 0, 0)

    def process_bind_param(self, value, dialect):
        return int((value - self.epoch).total_seconds() * self.divider)

    def process_result_value(self, value, dialect):
        return datetime.datetime.utcfromtimestamp(value / self.divider)


from .moz_places import Place
from .moz_bookmarks import (
    StructureItem,
    Folder,
    Separator,
    Bookmark,
    Tags,
    Tag,
    Unfiled,
    Places,
    Menu,
    Toolbar)

def connect(fpath):
    engine = create_engine("sqlite:///%s" % fpath)
    Base.prepare(engine)
    session = sessionmaker(bind=engine)()
    return engine, session

