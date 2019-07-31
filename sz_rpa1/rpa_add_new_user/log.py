# -- coding: utf-8 --
import time
import os
import traceback
from PIL import Image
from sz_rpa1.rpa_add_new_user.dama import getCodeText
from sz_rpa1.rpa_add_new_user.rpa_logging import logging_fun
from selenium import webdriver
from selenium.common.exceptions import NoAlertPresentException
from sz_rpa1.sz_rpa_batch_add.MyException import YzmErr
from selenium.webdriver.chrome.options import Options


class YzmError(Exception):
    pass


def get_driver_log(url):
    # 无界面
    # chrome_options = Options()
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--disable-gpu')
    # driver = webdriver.Chrome(chrome_options=chrome_options)
    option = webdriver.ChromeOptions()
    option.add_argument('disable-infobars')
    driver = webdriver.Chrome(chrome_options=option)
    driver.implicitly_wait(10)
    driver.get(url)
    time.sleep(1)
    # 截取验证码
    pt = os.getcwd() + '/err_info'
    driver.save_screenshot('%s/yzm.png' % pt)
    # driver.save_screenshot('./登录页面.png')
    # print("登录页面截图完毕")
    el = driver.find_element_by_id('validatecode1')
    time.sleep(0.2)
    # 有界面的坐标
    # left = el.location['x'] + 370
    # top = el.location['y'] + 100
    # right = el.location['x'] + el.size['width'] + 440
    # bot = el.location['y'] + el.size['height'] + 170
    # print(left, top, right, bot)
    # 无界面的坐标
    left = el.location['x']
    top = el.location['y']
    right = el.location['x'] + el.size['width']
    bot = el.location['y'] + el.size['height']
    pt = os.getcwd() + '/err_info'
    im = Image.open('%s/yzm.png' % pt)
    tu = im.crop((left, top, right, bot))
    tu.save('%s/yzm.png' % pt)
    # 登录次数
    num_list = []
    input_pwd_user(driver, num_list)
    if len(num_list) > 2:
        try:
            raise YzmErr("验证码有误")
        except YzmErr:
            # 记录异常日志
            logging = logging_fun()
            ret = traceback.format_exc()
            logging.error(ret)
            raise YzmErr("验证码有误")

    return driver


def input_pwd_user(driver, num_list):
    # 获取验证码
    pt = os.getcwd() + '/err_info/yzm.png'
    code_text = getCodeText('lipeishun', 'l638152', pt, 4004)
    input_user = driver.find_element_by_id("userNameInput")
    input_user.clear()
    # input_user.send_keys("537997")
    input_user.send_keys("428341")
    input_pwd = driver.find_element_by_id("userPwdInput")
    input_pwd.clear()
    # input_pwd.send_keys("SZjh2015")
    input_pwd.send_keys("Jk180912")
    yzm = driver.find_element_by_id("yzm")
    # time.sleep(7)
    yzm.clear()
    yzm.send_keys(code_text)
    # 登录详情截图
    pt = os.getcwd() + '/err_info'
    driver.save_screenshot('%s/log_detail.png' % pt)
    log_click = driver.find_element_by_class_name("btn-logon")
    log_click.click()
    try:
        driver.switch_to_alert().accept()
        num_list.append(1)
        if len(num_list) < 3:
            time.sleep(1)
            input_pwd_user(driver, num_list)

    except NoAlertPresentException:
        print('验证码正确')
