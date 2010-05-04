# Copyright (c) 2010 Infrae. All rights reserved.
# See also LICENSE.txt
# $Id$

import logging

from five import grok
from zeam.form import silva as silvaforms

from silva.security.logging.interfaces import (
    ILoggingStorage, ISQLStorageConfiguration, ILogger)

logger = logging.getLogger("silva.security.logging")



class PythonLogger(grok.GlobalUtility):
    grok.implements(ILoggingStorage, ILogger)
    grok.provides(ILoggingStorage)
    grok.name('Python Logger')

    storage_conf = silvaforms.Fields()

    def log(self, event):
        msg = '"%s" did %s %s'
        info = [event.username, event.action, event.content_path]
        if event.detail:
            msg += ' (%s)'
            info.append(event.detail)
        logger.info(msg % tuple(info))

    def configure(self, context):
        return self


class ZopeSQLLogger(object):
    """Log in a Zope SQL connection.
    """
    grok.implements(ILogger)

    def __init__(self, connection):
        self.connection = connection

    def log(self, event):
        db = self.connection()
        try:
            db.query("""insert into log
                        (username, action, time, content, content_intid, info)
                        values (%r, %r, now(), %r, %d, %r)""" % (
                    event.username, event.action,
                    event.content_path, event.content_id,
                    event.detail or ""))
        finally:
            db.close()


class ZopeSQLStorage(grok.GlobalUtility):
    grok.implements(ILoggingStorage)
    grok.provides(ILoggingStorage)
    grok.name('Zope SQL')

    storage_conf = silvaforms.Fields(ISQLStorageConfiguration)

    def configure(self, context):
        if 'sql_connection_id' not in context.storage_conf:
            logger.error('SQL logger not properly configured')
            return
        connection_id = context.storage_conf['sql_connection_id']
        try:
            connection = getattr(context, connection_id)
        except AttributeError:
            logger.error('SQL connection %s no longer exists' % connection_id)
        return ZopeSQLLogger(connection)
