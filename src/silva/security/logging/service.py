# Copyright (c) 2010 Infrae. All rights reserved.
# See also LICENSE.txt
# $Id$

from five import grok
from zope.component import getUtility

from silva.core import conf as silvaconf
from silva.core.services.base import SilvaService
from silva.security.logging.interfaces import (
    ISecurityLoggingService, ILoggingStorage)


class SecurityLoggingService(SilvaService):
    """Service to logging security events.
    """
    meta_type = "Silva Security Logging Service"
    default_service_identifier = 'service_securitylogging'
    grok.implements(ISecurityLoggingService)
    silvaconf.icon('service.png')

    def get_storage(self):
        return getUtility(ILoggingStorage, name="Python Logger")
