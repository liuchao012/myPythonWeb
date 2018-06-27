# -*- coding: utf-8 -*-
# @Time    : 2018/6/25 20:15
# @Author  : Mat
# @Email   : mat_wu@163.com
# @File    : functional_tests1.py
# @Software: PyCharm

from selenium import webdriver
import unittest


class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(3)

    def tearDown(self):
        self.driver.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        self.driver.get("http://localhost:8000")
        self.assertIn('To-Do', self.driver.title)
        # assert 'To-Do' in driver.title, "Browser title was:" + driver.title
        self.fail('Finisth the test')


if __name__ == '__main__':
    unittest.main(warnings='ignore')
