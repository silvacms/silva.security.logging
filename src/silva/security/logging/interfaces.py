# Copyright (c) 2010 Infrae. All rights reserved.
# See also LICENSE.txt
# $Id$

from five import grok
from zope import schema
from zope.component import getUtilitiesFor
from zope.interface import Interface, Attribute
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.schema.interfaces import IContextSourceBinder

from Products.ZSQLMethods.SQL import SQLConnectionIDs
from Acquisition import aq_inner

from silva.core.interfaces import ISilvaLocalService


class ISecurityEvent(Interface):
    """A security event.
    """


class ILoggingStorage(Interface):
    """Describe a logging storage.
    """
    storage_conf = Attribute(u"Configuration fields for this storage")

    def configure(context):
        """Return a logger for the given context.
        """


class ILogger(Interface):
    """A logger able to log an event.
    """

    def log(event):
        """Log the given event.
        """


@grok.provider(IContextSourceBinder)
def available_storages(context):
    return SimpleVocabulary(
        map(lambda (name, storage): SimpleTerm(value=name, title=name),
            getUtilitiesFor(ILoggingStorage)))


@grok.provider(IContextSourceBinder)
def available_sql_connections(context):
    return SimpleVocabulary(
        map(lambda (name, title): SimpleTerm(value=name, title=title),
            SQLConnectionIDs(aq_inner(context))))


class ISecurityLoggingConfiguration(Interface):
    """Configuration for the Security Logging service.
    """
    storage_name = schema.Choice(
        title=u"Log storage",
        source=available_storages)


class ISQLStorageConfiguration(Interface):
    """Configuration settings for the SQL storage
    """
    sql_connection_id = schema.Choice(
        title=u"SQL Connection",
        source=available_sql_connections)
    sql_table = schema.TextLine(
        title=u"SQL Table to use",
        default=u"log",
        required=True)


class ISecurityLoggingService(
    ISilvaLocalService, ISecurityLoggingConfiguration):
    """Local service to log security event.
    """
    storage_conf = Attribute(u"Configuration for the storage")

    def get_storage():
        """Return storage used to log events.
        """

    def get_logger():
        """Return storage's logger to log events.
        """
