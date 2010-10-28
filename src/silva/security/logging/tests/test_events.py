# -*- coding: utf-8 -*-
# Copyright (c) 2010 Infrae. All rights reserved.
# See also LICENSE.txt
# $Id$

import unittest

import DateTime
from Products.Silva.tests.helpers import publish_content

from zope.component import queryUtility
from silva.security.logging.testing import FunctionalLayer
from silva.security.logging.interfaces import ISecurityLoggingService


class AssertLog(object):

    def __init__(self, test, expected):
        self.test = test
        self.expected = expected

    def __enter__(self):
        self.test.logger.purge()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.test.assertEqual(self.expected, self.test.logger.records)
        self.test.logger.purge()


class SubscribersTestCase(unittest.TestCase):
    layer = FunctionalLayer

    def setUp(self):
        self.root = self.layer.get_application()
        self.layer.login('editor')

        factory = self.root.manage_addProduct['silva.security.logging']
        factory.manage_addSecurityLoggingService()

        service = queryUtility(ISecurityLoggingService)
        service.storage_name = 'Memory Logger (for testing)'
        self.logger = service.get_logger()

    def tearDown(self):
        self.logger.purge()

    def test_add_content(self):
        with AssertLog(
            self,
            [['editor', 'add', '/root/folder'],
             ['editor', 'modify the container', '/root'],
             ['editor', 'create', '/root/folder']]):
            factory = self.root.manage_addProduct['Silva']
            factory.manage_addFolder('folder', 'Folder')

    def test_copy_content(self):
        factory = self.root.manage_addProduct['Silva']
        factory.manage_addFolder('folder', 'Folder')

        with AssertLog(
            self,
            [['editor', 'copy', 'copy_of_folder', 'from /root/folder'],
             ['editor', 'add', '/root/copy_of_folder'],
             ['editor', 'modify the container', '/root']]):
            token = self.root.manage_copyObjects(['folder'])
            self.root.manage_pasteObjects(token)

    def test_rename_content(self):
        factory = self.root.manage_addProduct['Silva']
        factory.manage_addFolder('folder', 'Folder')

        with AssertLog(
            self,
            [['editor', 'move', '/root/news', 'from /root/folder to /root/news'],
             ['editor', 'modify the container', '/root']]):
            self.root.manage_renameObjects(['folder'], ['news'])

    def test_move_content(self):
        factory = self.root.manage_addProduct['Silva']
        factory.manage_addFolder('folder', 'Folder')
        factory.manage_addFolder('target', 'Target')

        with AssertLog(
            self,
            [['editor', 'move', '/root/target/folder', 'from /root/folder to /root/target/folder'],
             ['editor', 'modify the container', '/root'],
             ['editor', 'modify the container', '/root/target']]
):
            token = self.root.manage_cutObjects(['folder'])
            self.root.target.manage_pasteObjects(token)

    def test_delete_content(self):
        factory = self.root.manage_addProduct['Silva']
        factory.manage_addFolder('folder', 'Folder')

        with AssertLog(
            self,
            [['editor', 'delete', '/root/folder'],
             ['editor', 'modify the container', '/root']]):
            self.root.manage_delObjects(['folder'])

    def test_publication(self):
        factory = self.root.manage_addProduct['SilvaDocument']
        factory.manage_addDocument('document', 'Document')
        document = self.root.document

        with AssertLog(
            self,
            [['editor', 'publish', '/root/document/0']]):
            # First publication
            publish_content(document)

        with AssertLog(
            self,
            [['editor', 'add', '/root/document/1'],
             ['editor', 'modify the container', '/root/document']]):
            # Create copy
            document.create_copy()

        with AssertLog(
            self,
            [['editor', 'close', '/root/document/0'],
             ['editor', 'publish', '/root/document/1']]):
            # Publish copy (so close the published one first)
            publish_content(document)

    def test_request_approval(self):
        self.layer.login('author')
        factory = self.root.manage_addProduct['SilvaDocument']
        factory.manage_addDocument('document', 'Document')

        document = self.root.document
        document.set_unapproved_version_publication_datetime(
            DateTime.DateTime() - 10)

        with AssertLog(
            self,
            [['author', 'request approval', '/root/document/0']]):
            # Request approval
            document.request_version_approval('Ready')

        with AssertLog(
            self,
            [['author', 'cancel request approval', '/root/document/0']]):
            # Withdraw approval
            document.withdraw_version_approval('Not really ready')

        document.request_version_approval('Ready')
        self.layer.login('chiefeditor')

        with AssertLog(
            self,
            [['chiefeditor', 'cancel request approval', '/root/document/0']]):
            # Reject approval
            document.withdraw_version_approval('Not really ready')


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(SubscribersTestCase))
    return suite
