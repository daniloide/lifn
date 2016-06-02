#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re
import time
import os

HOME = os.path.expanduser("~")
WEB2PY_PATH=os.path.join( HOME, "workspace", "web2py" )

PROTO = "http"
HOST = "127.0.0.1"
PORT = 8000
APP_NAME = "lifn"
BASE_URL = "%s://%s:%s/%s" % (PROTO, HOST, PORT, APP_NAME)

class TestFirstRun(unittest.TestCase):

    def __deleteDir(self, dirName = os.path.join(WEB2PY_PATH, "applications", APP_NAME, "databases") ):
        if dirName=="/":
            return
        print("Deleteing: %s" % dirName)
        for root, dirs, files in os.walk(dirName, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()
        self.driver.implicitly_wait(30)
        self.base_url = BASE_URL
        self.verificationErrors = []
        self.accept_next_alert = True


    def test_a001_first_run(self):
        self.__deleteDir()
        driver = self.driver
        driver.get(self.base_url + "/default/firstRun")
        self.assertEqual("Inventario Forestal Nacional", driver.title)
        driver.find_element_by_id("auth_user_username").clear()
        driver.find_element_by_id("auth_user_username").send_keys("admin")
        driver.find_element_by_id("auth_user_first_name").clear()
        driver.find_element_by_id("auth_user_first_name").send_keys("Admin")
        driver.find_element_by_id("auth_user_last_name").clear()
        driver.find_element_by_id("auth_user_last_name").send_keys("Admin")
        driver.find_element_by_id("auth_user_email").clear()
        driver.find_element_by_id("auth_user_email").send_keys("admin@admin.com")
        driver.find_element_by_id("auth_user_password").clear()
        driver.find_element_by_id("auth_user_password").send_keys("12")
        driver.find_element_by_id("confirmP").clear()
        driver.find_element_by_id("confirmP").send_keys("12")
        driver.find_element_by_css_selector("input.btn").click()
        self.assertEqual(self.base_url + "/default/user/login", driver.current_url)

    def test_a002_first_login(self):
        driver = self.driver
        driver.get(self.base_url + "/default/user/login")
        self.assertEqual("Inventario Forestal Nacional", driver.title)
        driver.find_element_by_id("auth_user_username").clear()
        driver.find_element_by_id("auth_user_username").send_keys("admin")
        driver.find_element_by_id("auth_user_password").clear()
        driver.find_element_by_id("auth_user_password").send_keys("12")
        driver.find_element_by_id("auth_user_remember").click()
        driver.find_element_by_css_selector("input.btn").click()
        time.sleep(5)
        self.assertEqual(self.base_url + "/default/loadTypes", driver.current_url)


    def test_a003_loadSamples(self):
        driver = self.driver
        driver.get(self.base_url + "/default/user/login")
        self.assertEqual("Inventario Forestal Nacional", driver.title)
        driver.find_element_by_id("auth_user_username").clear()
        driver.find_element_by_id("auth_user_username").send_keys("admin")
        driver.find_element_by_id("auth_user_password").clear()
        driver.find_element_by_id("auth_user_password").send_keys("12")
        driver.find_element_by_id("auth_user_remember").click()
        driver.find_element_by_css_selector("input.btn").click()
        self.assertEqual(self.base_url + "/default/index", driver.current_url)
        driver.get(self.base_url + "/default/loadNewSamples")
        fileInput = driver.find_element_by_xpath("//input[@name='file' and @type='file']")
        fileInput.send_keys("/home/fpacheco/workspace/lifn/tests/xml/test1_small_2014.xml")
        time.sleep(5)
        driver.find_element_by_xpath("//input[@value='Guardar' and @type='submit']").click()
        self.assertEqual("Inventario Forestal Nacional", driver.title)


    def test_a004_asignMuestreos(self):
        driver = self.driver
        driver.get(self.base_url + "/default/user/login")
        self.assertEqual("Inventario Forestal Nacional", driver.title)
        driver.find_element_by_id("auth_user_username").clear()
        driver.find_element_by_id("auth_user_username").send_keys("admin")
        driver.find_element_by_id("auth_user_password").clear()
        driver.find_element_by_id("auth_user_password").send_keys("12")
        driver.find_element_by_id("auth_user_remember").click()
        driver.find_element_by_css_selector("input.btn").click()
        self.assertEqual(self.base_url + "/default/index", driver.current_url)
        driver.get(self.base_url + "/default/muestreoUsuarios")
        driver.find_element_by_xpath("//input[@name='selectAll' and @type='button']").click()
        driver.find_element_by_xpath("//input[@id='guardar' and @type='button']").click()
        driver.get(self.base_url + "/default/index")
        cell = driver.find_element_by_xpath("//div[@class='web2py_table']//table//tbody//tr/td[contains(text(), 'U080')]")
        print cell
        self.assertEqual("U080", cell.text)


    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True

    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException, e: return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
