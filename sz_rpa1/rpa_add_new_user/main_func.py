import time
import traceback
from sz_rpa1.rpa_add_new_user.get_element import get_element_by_id_send, get_element_by_id_click
from sz_rpa1.rpa_add_new_user.get_element import get_element_by_class_click, get_element_by_class_send
from sz_rpa1.rpa_add_new_user.get_element import get_element_by_name_click, get_element_by_name_send
from sz_rpa1.rpa_add_new_user.chose_time.rs_time import chose_time
from sz_rpa1.rpa_add_new_user.log import get_driver_log
from sz_rpa1.rpa_add_new_user.get_element import get_element_by_xpath_click, get_element_by_xpath_send
from sz_rpa1.rpa_add_new_user.get_element import get_element_by_selector_click
from selenium.common.exceptions import NoSuchElementException
from sz_rpa1.rpa_add_new_user.delayed import ErrorUser, ErrorPage
from sz_rpa1.rpa_add_new_user.rpa_logging import logging_fun
from sz_rpa1.rpa_add_new_user.connect_mysql import read_data, update_data
from selenium.common.exceptions import NoAlertPresentException
from sz_rpa1.sz_rpa_batch_add.MyException import CloseWindowErr


def add_user():
    # 登录
    url = 'https://sipub.sz.gov.cn/hsoms/logonDialog.jsp'
    driver = get_driver_log(url)
    # 关闭弹窗
    time.sleep(100000)
    close_window(driver)
    sql = "select * from shenzhen_add where status=0 limit %d, %d" % (0, 4)
    # 拿到的批量数据信息
    user_info = read_data(sql)
    # open_info_page(driver, user_info)
    # 单条录入信息
    # print(user_info)
    for info in user_info:
        try:
            open_info_page(driver, info)
        except:
            pass
            # print('验证码有误')
        try:
            tuichu(driver)
        except:
            pass


def close_window(driver):
    time.sleep(2)
    # driver.save_screenshot('./登录跳转.png')
    # print("跳转页面截图完毕")
    try:
        el = driver.find_elements_by_class_name("dw-res-wnd-header-closebtn-ext")[1]
        el.click()
        time.sleep(0.5)
        el = driver.find_element_by_class_name("dw-res-wnd-header-closebtn-ext")
        el.click()
    except NoSuchElementException:
        # print('关闭窗口NoSuchElementException异常, 重新刷新')
        driver.refresh()
        time.sleep(3)
        el = driver.find_elements_by_class_name("dw-res-wnd-header-closebtn-ext")[1]
        el.click()
        time.sleep(3)
        el = driver.find_element_by_class_name("dw-res-wnd-header-closebtn-ext")
        el.click()
    except:
        try:
            raise CloseWindowErr("关闭弹窗错误")
        except:
            logging = logging_fun()
            ret = traceback.format_exc()
            logging.error(ret)


def open_info_page(driver, info):
    '''
    打开信息页面
    '''
    time.sleep(1)
    # driver.save_screenshot('./登录跳转.png')
    # print("跳转页面截图完毕")
    try:
        # 参保管理
        cbgl = driver.find_element_by_id("returnYwsb('F02000')")
        cbgl.click()
        # 新增职工参加社会保险申报
        xzsb = driver.find_element_by_id('grcbdjgl-p1')
        xzsb.click()
    except NoSuchElementException:
        print('打开输入信息页异常NoSuchElementException异常, 重新刷新')
        driver.refresh()
        time.sleep(3)
        # 重新关闭弹窗
        close_window(driver)
        time.sleep(0.5)
        # 参保管理
        cbgl = driver.find_element_by_id("returnYwsb('F02000')")
        cbgl.click()
        # 新增社保
        xzsb = driver.find_element_by_id('grcbdjgl-p1')
        xzsb.click()
    except:
        print("异常， 关闭浏览器")
        driver.quit()
        raise
    # 在填入信息的时候出现错误
    try:
        write_info(driver, info)
        # 信息完成， 修改状态
        update_sql = "update shenzhen_add set status = 1 where identity_no = '%s'" % info[1]
        update_data(update_sql)
    except ErrorPage:
        # driver.save_screenshot('./erro_page.png')
        update_sql = "update shenzhen_add set reason = '获取不到页面元素' where identity_no = '%s'" % info[1]
        update_data(update_sql)
    except:
        # 关闭弹窗信息，并写入日志
        try:
            driver.switch_to_alert().dismiss()
        except NoAlertPresentException:
            # 没有弹窗
            pass
        # driver.save_screenshot('./other_error.png')
        logging = logging_fun()
        ret = traceback.format_exc()
        logging.error(ret)
        # 重新增加用户
        # from rpa_add_new_user.main_func import open_info_page, close_window, write_info
        user_info = info[1]
        query_sql = "select err_num from shenzhen_add where identity_no = '%s'" % user_info
        err_num = read_data(query_sql)[0][0]
        err_num += 1
        if err_num < 3:
            print('err_num', err_num)
            # 修改数据库中的错误次数
            update_sql = "update shenzhen_add set err_num = %s where identity_no = '%s'" % (err_num, user_info)
            update_data(update_sql)
            driver.refresh()
            time.sleep(4)
            close_window(driver)
            open_info_page(driver, info)
        update_sql = "update shenzhen_add set reason = '用户信息有误' where identity_no = '%s'" % info[1]
        update_data(update_sql)


def write_info(driver, info):
    get_element_by_class_send(driver, "dw-sform-textinput-widget-ext", info[1])
    get_element_by_name_send(driver, "cszjhm", info[1])
    get_element_by_name_send(driver, 'xm', info[2])
    time.sleep(0.3)
    get_element_by_name_click(driver, 'query')
    time.sleep(1)
    # 点开民族
    get_element_by_xpath_click(driver,
                               '//tbody/tr[3]/td[1]/table[@class="dw-sform-extdropdwon"]/tbody/tr/td[2]/div/table/tbody/tr/td[1]/input[2]')
    time.sleep(0.5)
    # 获取标签原内容
    try:
        old_content_na = driver.find_elements_by_class_name("dw-sform-extdropdwon-showbox-items-item-focus")
    except:
        pass
    na = info[6]
    if old_content_na[0].text != na:
        get_element_by_selector_click(driver, 'div[class="dw-sform-extdropdwon-showbox-items-item-text"][title=%s]', na)
    else:
        old_content_na[0].click()
    # 点开户籍
    get_element_by_xpath_click(driver,
                               '//tbody/tr[3]/td[4]/table[@class="dw-sform-extdropdwon"]/tbody/tr/td[2]/div/table/tbody/tr/td[1]/input[2]')
    old_content_hj = driver.find_elements_by_class_name("dw-sform-extdropdwon-showbox-items-item-focus")
    hj = info[8]
    if old_content_hj[1].text != hj:
        get_element_by_selector_click(driver, 'div[class="dw-sform-extdropdwon-showbox-items-item-text"][title=%s]', hj)
    else:
        old_content_hj[1].click()
    time.sleep(0.5)
    # 点开入深时间 / 填入入深时间
    driver.find_elements_by_css_selector('.dw-sform-textinput-datePicBtn-ext')[1].click()
    time.sleep(0.5)
    # 点开年份
    get_element_by_id_click(driver, 'laydate_y')
    # 选择年份
    time.sleep(0.5)
    # y = 2053
    date = info[9]
    y = date.year
    m = date.month
    d = date.day

    if y >= 1956 and y <= 1969:
        chose_time(1956, driver, y, m, d)
    elif y >= 1970 and y <= 1983:
        chose_time(1970, driver, y, m, d)
    elif y >= 1984 and y <= 1997:
        chose_time(1984, driver, y, m, d)
    elif y >= 1998 and y <= 2011:
        chose_time(1984, driver, y, m, d)
    elif y >= 2012 and y <= 2025:
        chose_time(2012, driver, y, m, d)
    elif y >= 2026 and y <= 2039:
        chose_time(2026, driver, y, m, d)
    elif y >= 2040 and y <= 2053:
        chose_time(2040, driver, y, m, d)
    # 填手机号码/地址
    time.sleep(0.5)
    # number = 16356782194
    number = info[10]
    get_element_by_name_send(driver, 'sjhm', number)
    # time.sleep(1)
    # 通讯地址
    addr = info[12]
    # print("通讯地址", addr)
    get_element_by_name_send(driver, 'txdz', addr)
    # 选择个人身份/ 职工性质/ 缴费工资
    time.sleep(0.5)
    get_element_by_xpath_click(driver,
                               '//tbody/tr[6]/td[1]/table[@class="dw-sform-extdropdwon"]/tbody/tr/td[2]/div/table/tbody/tr/td[1]/input[2]')
    sf = info[14]
    old_content_sf = driver.find_elements_by_class_name("dw-sform-extdropdwon-showbox-items-item-focus")

    if old_content_sf[2].text != sf:
        get_element_by_selector_click(driver, 'div[class="dw-sform-extdropdwon-showbox-items-item-text"][title=%s]', sf)
    else:
        old_content_sf[2].click()
    # 缴费工资
    salary = round(info[16])
    get_element_by_name_send(driver, 'jfjs', salary)
    # 职工性质
    get_element_by_xpath_click(driver,
                               '//tbody/tr[6]/td[2]/table[@class="dw-sform-extdropdwon"]/tbody/tr/td[2]/div/table/tbody/tr/td[1]/input[2]')
    old_content_zg = driver.find_elements_by_class_name("dw-sform-extdropdwon-showbox-items-item-focus")
    zg = info[15]
    if old_content_zg[3].text != zg:
        driver.find_element_by_css_selector('div[class="dw-sform-extdropdwon-showbox-items-item-text"][title=%s]' % zg)
    else:
        old_content_zg[3].click()

    # 学历 / 参保年月
    # 展开学历
    time.sleep(0.6)
    get_element_by_xpath_click(driver,
                               '//tbody/tr[7]/td[1]/table[@class="dw-sform-extdropdwon"]/tbody/tr/td[2]/div/table/tbody/tr/td[1]/input[2]')
    time.sleep(0.5)
    old_content_xl = driver.find_elements_by_class_name("dw-sform-extdropdwon-showbox-items-item-focus")
    xl = info[17]
    if old_content_xl[4].text != xl:
        get_element_by_selector_click(driver, 'div[class="dw-sform-extdropdwon-showbox-items-item-text"][title=%s]', xl)
    else:
        old_content_xl[4].click()
    print("信息填完")


def tuichu(driver):
    time.sleep(1)
    driver.find_element_by_class_name("dw-res-wnd-header-closebtn-ext").click()
    time.sleep(1)


if __name__ == '__main__':
    add_user()
