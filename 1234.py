# -*- encoding=utf8 -*-
__author__ = "Administrator"

from airtest.core.api import *
auto_setup(__file__)

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from airtest_selenium.proxy import WebChrome
driver = WebChrome()
driver.implicitly_wait(20)

driver.get("https://www.baidu.com/")
driver.find_element_by_id("kw").send_keys("python")
driver.find_element_by_xpath("//input[@type='submit']").click()

driver.airtest_touch(Template(r"tpl1572855091291.png", record_pos=(1.675, 5.34), resolution=(100, 100)))

driver.switch_to_new_tab()
driver.find_element_by_xpath("//*[@id=\"downloads\"]/a").click()
driver.assert_exist("//*[@id=\"touchnav-wrapper\"]/header/div/div[2]/div/div[4]/p/a", "xpath", "找到了下载按钮.")
driver.assert_template(Template(r"tpl1572855916818.png", record_pos=(0.895, 6.645), resolution=(100, 100)), "找到下载")
driver.quit()



