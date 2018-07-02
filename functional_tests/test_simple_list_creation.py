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


class NewVisitorTest(FunctionalTest):

    def test_can_start_a_list_and_retrieve_it_later(self):
        # 类继承LiveServerTestCase 后将不使用实际部署的localhost 地址,使用 django提供的self.live_server_url地址
        # self.driver.get("http://localhost:8000")
        self.driver.get(self.live_server_url)

        # 发现页面上显示的 TO-DO 字样
        self.assertIn('To-Do', self.driver.title)
        header_text = self.driver.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # 应用邀请输入一个代办事项
        inputbox = self.driver.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do item')

        # 在输入框中输入购买孔雀羽毛
        inputbox.send_keys('Buy peacock feathers')

        # 点击回车后页面更新
        # 代办事项中显示 ‘1：Buy peacock feathers’
        inputbox.send_keys(Keys.ENTER)

        edith_list_url = self.driver.current_url
        self.assertRegex(edith_list_url, '/list/.+?')

        table = self.driver.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        # self.assertTrue(any(row.text == '1：Buy peacock feathers' for row in rows), 'New to-do item did not appear in table - - its text was:\n%s' % (table.text))

        # 页面又显示了一个文本框，可以输入其他代办事项
        # 输入‘Use peacock feathers to make a fly’
        inputbox = self.driver.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)
        table = self.driver.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn('1：Buy peacock feathers', [row.text for row in rows])
        self.assertIn('2：Use peacock feathers to make a fly', [row.text for row in rows])

        ##我们需要新打开一个浏览器，并且不让cookice相互干扰
        # 让录入的清单不会被别人看到
        self.driver.quit()

        # 其他人访问页面看不到刚才录入的清单
        self.driver = webdriver.Firefox()
        self.driver.get(self.live_server_url)
        page_text = self.driver.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        # 他输入了新的代办事项，创建了一个新的代办清单
        inputbox = self.driver.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)

        # 他获得了一个属于他自己的url
        francis_list_url = self.driver.current_url
        self.assertRegex(edith_list_url, '/list/.+?')
        self.assertNotEquals(francis_list_url, edith_list_url)

        # 这个页面还是没有其他人的清单
        # 但是这个页面包含他自己的清单
        page_text = self.driver.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)
        # self.fail('Finisth the test')
