# -*- coding: utf-8 -*-
# @Time    : 2018/6/25 20:15
# @Author  : Mat
# @Email   : mat_wu@163.com
# @File    : functional_tests1.py
# @Software: PyCharm

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest


class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(3)

    def tearDown(self):
        self.driver.quit()
    def check_for_row_in_list_table(self, row_text):
        table = self.driver.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        self.driver.get("http://localhost:8000")

        #发现页面上显示的 TO-DO 字样
        self.assertIn('To-Do', self.driver.title)
        header_text = self.driver.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        #应用邀请输入一个代办事项
        inputbox=self.driver.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do item')

        #在输入框中输入购买孔雀羽毛
        inputbox.send_keys('Buy peacock feathers')

        #点击回车后页面更新
        #代办事项中显示 ‘1：Buy peacock feathers’
        inputbox.send_keys(Keys.ENTER)

        table = self.driver.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        #self.assertTrue(any(row.text == '1：Buy peacock feathers' for row in rows), 'New to-do item did not appear in table - - its text was:\n%s' % (table.text))

        #页面又显示了一个文本框，可以输入其他代办事项
        #输入‘Use peacock feathers to make a fly’
        inputbox = self.driver.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)
        table = self.driver.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn('1：Buy peacock feathers', [row.text for row in rows])
        self.assertIn('2：Use peacock feathers to make a fly', [row.text for row in rows])

        self.fail('Finisth the test')


if __name__ == '__main__':
    unittest.main(warnings='ignore')

