import time
from selenium import webdriver
from sz_rpa1.rpa_add_new_user.delayed import wrapper_commit_ago


def get_driver(url):
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    driver.get(url)
    time.sleep(1)
    return driver


@wrapper_commit_ago
def get_element_by_id_send(driver, id_name, content=None):
    el = driver.find_element_by_id(id_name)
    el.clear()
    el.send_keys(content)


@wrapper_commit_ago
def get_element_by_id_click(driver, id_name):
    el = driver.find_element_by_id(id_name)
    el.click()


@wrapper_commit_ago
def get_element_by_class_click(driver, class_name):
    el = driver.find_element_by_class_name(class_name)
    el.click()


@wrapper_commit_ago
def get_element_by_class_send(driver, class_name, content=None):
    el = driver.find_element_by_class_name(class_name)
    el.clear()
    el.send_keys(content)


@wrapper_commit_ago
def get_element_by_name_send(driver, name, content=None):
    el = driver.find_element_by_name(name)
    el.clear()
    el.send_keys(content)


@wrapper_commit_ago
def get_element_by_name_click(driver, name):
    el = driver.find_element_by_name(name)
    el.click()


@wrapper_commit_ago
def get_element_by_xpath_click(driver, name):
    el = driver.find_element_by_xpath(name)
    el.click()


@wrapper_commit_ago
def get_element_by_xpath_send(driver, name, content=None):
    el = driver.find_element_by_xpath(name)
    el.clear()
    el.send_keys(content)


@wrapper_commit_ago
def get_element_by_selector_click(driver, name, parameter):
    el = driver.find_element_by_css_selector(name % parameter)
    el.click()


@wrapper_commit_ago
def get_element_by_selector_send(driver, name, content=None):
    el = driver.find_element_by_css_selector(name)
    el.clear()
    el.send_keys(content)
