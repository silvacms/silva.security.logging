# Copyright (c) 2010 Infrae. All rights reserved.
# See also LICENSE.txt
# $Id$

from five import grok
from zope.app.container.interfaces import (
    IObjectMovedEvent, IObjectAddedEvent, IObjectRemovedEvent)
from zope.lifecycleevent.interfaces import (
    IObjectCreatedEvent, IObjectCopiedEvent, IObjectModifiedEvent)


from OFS.interfaces import IObjectWillBeRemovedEvent

from silva.security.logging.entry import SecurityEvent, get_path
from silva.core.interfaces import events
from silva.core.interfaces import ISilvaObject, IContent


@grok.subscribe(ISilvaObject, IObjectCreatedEvent)
def log_create(content, event):
    if IObjectCopiedEvent.providedBy(event):
        detail = 'from %s' % get_path(event.original)
        SecurityEvent('copy', content, detail).log()
    else:
        SecurityEvent('create', content).log()


@grok.subscribe(ISilvaObject, IObjectWillBeRemovedEvent)
def log_delete(content, event):
    if content is event.object:
        SecurityEvent('delete', content).log()


@grok.subscribe(ISilvaObject, IObjectAddedEvent)
def log_add(content, event):
    if content is event.object:
        SecurityEvent('add', content).log()


@grok.subscribe(ISilvaObject, IObjectModifiedEvent)
def log_modify(content, event):
    SecurityEvent('modify', content).log()


@grok.subscribe(ISilvaObject, IObjectMovedEvent)
def log_move(content, event):
    if content is event.object:
        if not (IObjectAddedEvent.providedBy(event) or
                IObjectRemovedEvent.providedBy(event)):
            detail = 'from %s/%s to %s/%s' % (
                get_path(event.oldParent), event.oldName,
                get_path(event.newParent), event.newName)
            SecurityEvent('move', content, detail).log()
