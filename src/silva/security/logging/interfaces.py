# Copyright (c) 2010 Infrae. All rights reserved.
# See also LICENSE.txt
# $Id$

from zope.interface import Interface, Attribute
from silva.core.interfaces import ISilvaLocalService


class ISecurityLoggingService(ISilvaLocalService):
    """Local service to log security event.
    """

    def get_storage():
        """Return storage used to log events.
        """


class ISecurityEvent(Interface):
    """A security event.
    """


class ILoggingStorage(Interface):
    """Describe a logging storage.
    """

    def log(event):
        """Log the given event.
        """
