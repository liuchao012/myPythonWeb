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
    def test_cannot_add_empty_list_items(self):
        self.driver.get(self.live_server_url)
        self.driver.find_element_by_id('id_new_item').send_keys('\n')
        error = self.driver.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "You cant have an empty list item")

        self.driver.find_element_by_id('id_new_item').send_keys('Buy milk\n')
        self.check_for_row_in_list_table('1：Buy milk')

        self.driver.find_element_by_id('id_new_item').send_keys('\n')
        self.check_for_row_in_list_table('1：Buy milk')
        error = self.driver.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "You cant have an empty list item")

        self.driver.find_element_by_id('id_new_item').send_keys('Buy tea\n')
        self.check_for_row_in_list_table('1：Buy milk')
        self.check_for_row_in_list_table('2：Buy tea')
        self.fail("write me!")
