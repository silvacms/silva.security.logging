# Copyright (c) 2010 Infrae. All rights reserved.
# See also LICENSE.txt
# $Id$

from AccessControl import getSecurityManager

from five import grok
from zope.app.intid.interfaces import IIntIds
from zope.component import queryUtility

from silva.security.logging.interfaces import (
    ISecurityEvent, ISecurityLoggingService)


def get_username():
    """Return the username of the current user.
    """
    return getSecurityManager().getUser().getUserName()


def get_path(content):
    """Return the path in Zope for the content.
    """
    return '/'.join(content.getPhysicalPath())


def get_id(content):
    """Return an unique identifier for the content, in order to be
    able to find it again even if it moves.
    """
    service = queryUtility(IIntIds)
    if service is not None:
        return service.register(content)
    return None


class SecurityEvent(object):
    """Represent an event.
    """
    grok.implements(ISecurityEvent)

    def __init__(self, action, content, detail=None):
        self.action = action
        self.username = get_username()
        self.content_path = get_path(content)
        self.content_id = get_id(content)
        self.detail = detail

    def log(self):
        service = queryUtility(ISecurityLoggingService)
        if service is not None:
            logger = service.get_logger()
            logger.log(self)

