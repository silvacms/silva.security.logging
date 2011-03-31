# Copyright (c) 2010 Infrae. All rights reserved.
# See also LICENSE.txt
# $Id$

from five import grok
from zope.container.interfaces import (
    IObjectMovedEvent, IObjectAddedEvent, IObjectRemovedEvent,
    IContainerModifiedEvent)
from zope.lifecycleevent.interfaces import (
    IObjectCreatedEvent, IObjectCopiedEvent, IObjectModifiedEvent)

from OFS.interfaces import IObjectWillBeRemovedEvent

from silva.security.logging.entry import SecurityEvent, get_path
from silva.core.interfaces import events
from silva.core.interfaces import ISilvaObject, IVersion


@grok.subscribe(ISilvaObject, IObjectCreatedEvent)
def log_create(content, event):
    if IObjectCopiedEvent.providedBy(event):
        detail = 'from %s' % get_path(event.original)
        SecurityEvent('copy', content, detail).log()
    else:
        SecurityEvent('create', content).log()


@grok.subscribe(IVersion, IObjectWillBeRemovedEvent)
@grok.subscribe(ISilvaObject, IObjectWillBeRemovedEvent)
def log_delete(content, event):
    if content is event.object:
        SecurityEvent('delete', content).log()


@grok.subscribe(IVersion, IObjectAddedEvent)
@grok.subscribe(ISilvaObject, IObjectAddedEvent)
def log_add(content, event):
    if content is event.object:
        SecurityEvent('add', content).log()


@grok.subscribe(IVersion, IObjectModifiedEvent)
@grok.subscribe(ISilvaObject, IObjectModifiedEvent)
def log_modify(content, event):
    if IContainerModifiedEvent.providedBy(event):
        SecurityEvent('modify the container', content).log()
    else:
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


@grok.subscribe(ISilvaObject, events.ISecurityRestrictionModifiedEvent)
def log_security_restriction_set(content, event):
    if event.role:
        detail = 'with role %s' % event.role
        SecurityEvent('set a access restriction to', content, detail).log()
    else:
        SecurityEvent('remove the access restriction to', content).log()


@grok.subscribe(ISilvaObject, events.ISecurityRoleAddedEvent)
def log_security_add_role(content, event):
    detail = 'for %r roles %s' % (event.username, ', '.join(event.roles))
    SecurityEvent('changed roles on', content, detail).log()


@grok.subscribe(ISilvaObject, events.ISecurityRoleRemovedEvent)
def log_security_remove_role(content, event):
    detail = 'for %r' % event.username
    if event.roles:
        detail += ' roles %s' % ', '.join(event.roles)
    SecurityEvent('removed roles on', content, detail).log()


@grok.subscribe(IVersion, events.IContentRequestApprovalEvent)
def log_publication_request_approval(content, event):
    SecurityEvent('request approval', content).log()


@grok.subscribe(IVersion, events.IContentApprovalRequestWithdrawnEvent)
def log_publication_approval_request_cancel(content, event):
    SecurityEvent('cancel request approval', content).log()


@grok.subscribe(IVersion, events.IContentApprovalRequestRefusedEvent)
def log_publication_approval_request_refused(content, event):
    SecurityEvent('refuse request approval', content).log()


@grok.subscribe(IVersion, events.IContentPublishedEvent)
def log_publication_published(content, event):
    SecurityEvent('publish', content).log()


@grok.subscribe(IVersion, events.IContentClosedEvent)
def log_publication_closed(content, event):
    SecurityEvent('close', content).log()
