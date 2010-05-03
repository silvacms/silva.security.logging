# Copyright (c) 2010 Infrae. All rights reserved.
# See also LICENSE.txt
# $Id$

from five import grok
from zope import schema
from zope.component import getUtilitiesFor
from zope.interface import Interface, Attribute
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.schema.interfaces import IContextSourceBinder

from silva.core.interfaces import ISilvaLocalService


class ISecurityEvent(Interface):
    """A security event.
    """


class ILoggingStorage(Interface):
    """Describe a logging storage.
    """

    def log(event):
        """Log the given event.
        """


@grok.provider(IContextSourceBinder)
def available_storages(context):
    return SimpleVocabulary(
        map(lambda (name, storage): SimpleTerm(value=name, title=name),
            getUtilitiesFor(ILoggingStorage)))


class ISecurityLoggingConfiguration(Interface):
    """Configuration for the Security Logging service.
    """

    storage_name = schema.Choice(
        title=u"Log storage",
        source=available_storages)


class ISecurityLoggingService(
    ISilvaLocalService, ISecurityLoggingConfiguration):
    """Local service to log security event.
    """

    def get_storage():
        """Return storage used to log events.
        """
