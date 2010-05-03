# Copyright (c) 2010 Infrae. All rights reserved.
# See also LICENSE.txt
# $Id$

from five import grok
from zope.component import getUtility
from zeam.form import silva as silvaforms

from silva.core import conf as silvaconf
from silva.core.views import views as silvaviews
from silva.core.services.base import SilvaService
from silva.security.logging.interfaces import (
    ISecurityLoggingService, ILoggingStorage, ISecurityLoggingConfiguration)


class SecurityLoggingService(SilvaService):
    """Service to logging security events.
    """
    meta_type = "Silva Security Logging Service"
    default_service_identifier = 'service_securitylogging'
    grok.implements(ISecurityLoggingService)
    silvaconf.icon('service.png')

    manage_options = (
        {'label': 'Access log', 'action': 'manage_main'},
        {'label': 'Configuration', 'action': 'manage_config'},
        ) + SilvaService.manage_options

    storage_name = "Python Logger"
    storage_conf = {}

    def get_storage(self):
        if not hasattr(self, '_v_storage'):
            self._v_storage = getUtility(
                ILoggingStorage, name=self.storage_name)
        return self._v_storage



class ViewLog(silvaviews.ZMIView):
    """View logs.
    """
    grok.name('manage_main')

    def update(self):
        self.is_viewable = False


class Configuration(silvaforms.ZMIComposedForm):
    """Configure service.
    """
    grok.name('manage_config')

    label = u"Change configuration"
    description = u"Modify storage and storage options"



class SelectStorage(silvaforms.SubForm):
    silvaforms.view(Configuration)

    label = u"Select storage to use"
    fields = silvaforms.Fields(ISecurityLoggingConfiguration)
    actions = silvaforms.Actions(silvaforms.EditAction(u"Change"))
