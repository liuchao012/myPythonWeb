# -*- coding: utf-8 -*-
# @Time    : 2018/6/25 20:15
# @Author  : Mat
# @Email   : mat_wu@163.com
# @Software: PyCharm

from selenium import webdriver

driver = webdriver.Firefox()
driver.get("http://localhost:8000")
assert 'Django' in driver.title

