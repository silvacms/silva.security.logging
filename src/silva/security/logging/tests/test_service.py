# Copyright (c) 2010 Infrae. All rights reserved.
# See also LICENSE.txt
# $Id$

import unittest

from Products.Silva.testing import SilvaLayer

from zope.component import queryUtility
from zope.interface.verify import verifyObject
from silva.security.logging.interfaces import ISecurityLoggingService
import silva.security.logging


class ServiceTestCase(unittest.TestCase):

    layer = SilvaLayer(silva.security.logging)

    def setUp(self):
        self.root = self.layer.get_application()

    def test_add(self):
        """We add a service and check we can retrieve it.
        """
        self.failIf(hasattr(self.root, 'service_securitylogging'))
        service = queryUtility(ISecurityLoggingService)
        self.assertEqual(None, service)

        factory = self.root.manage_addProduct['silva.security.logging']
        factory.manage_addSecurityLoggingService()
        self.failUnless(hasattr(self.root, 'service_securitylogging'))

        service = queryUtility(ISecurityLoggingService)
        self.assertEqual(self.root.service_securitylogging, service)
        self.failUnless(verifyObject(ISecurityLoggingService, service))

        self.root.manage_delObjects(['service_securitylogging'])
        service = queryUtility(ISecurityLoggingService)
        self.assertEqual(None, service)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ServiceTestCase))
    return suite
