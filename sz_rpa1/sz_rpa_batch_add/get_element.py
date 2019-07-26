from sz_rpa1.rpa_add_new_user.delayed import wrapper_open_page


@wrapper_open_page
def get_element_by_name_click(driver, name):
    el = driver.find_element_by_name(name)
    el.click()


@wrapper_open_page
def get_element_by_name_send(driver, name, content=None):
    el = driver.find_element_by_name(name)
    el.send_keys(content)


@wrapper_open_page
def get_element_by_id_click(driver, name):
    el = driver.find_element_by_id(name)
    el.click()


@wrapper_open_page
def get_element_by_id_send(driver, name, content=None):
    el = driver.find_element_by_id(name)
    el.send_keys(content)


@wrapper_open_page
def get_element_by_class_name_click(driver, name):
    el = driver.find_element_by_class_name(name)
    el.click()


@wrapper_open_page
def get_element_by_class_name_send(driver, name, content=None):
    el = driver.find_element_by_class_name(name)
    el.send_keys(content)
