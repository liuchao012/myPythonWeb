# -*- coding: utf-8 -*-
# @Time    : 2018/6/25 20:15
# @Author  : Mat
# @Email   : mat_wu@163.com
# @File    : functional_tests1.py
# @Software: PyCharm

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import unittest
from unittest import skip
from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):
    @skip
    def test_cannot_add_empty_list_items(self):
        self.fail("write me!")
