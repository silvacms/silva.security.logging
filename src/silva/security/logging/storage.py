# Copyright (c) 2010 Infrae. All rights reserved.
# See also LICENSE.txt
# $Id$

import logging

from five import grok

from silva.security.logging.interfaces import ILoggingStorage

logger = logging.getLogger("silva.security.logging")



class PythonLogger(grok.GlobalUtility):
    grok.implements(ILoggingStorage)
    grok.name('Python Logger')

    def log(self, event):
        msg = '"%s" did %s %s'
        info = [event.username, event.action, event.content_path]
        if event.detail:
            msg += ' (%s)'
            info.append(event.detail)
        logger.info(msg % tuple(info))
