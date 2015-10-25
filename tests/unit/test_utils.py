#!/usr/bin/env python
#-*- coding:utf-8 -*-
# Author: Kun Huang <academicgareth@gmail.com>

from oslotest import base

class TestCase(base.BaseTestCase):
    def setUp(self):
        super(TestCase, self).setUp()

    def test_run(self):
        self.assertTrue(1)
