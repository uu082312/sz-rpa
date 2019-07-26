# -- coding: utf-8 --
import time
import os
import traceback
from sz_rpa1.rpa_add_new_user.rpa_logging import logging_fun
from sz_rpa1.sz_rpa_batch_add.delayed import wrapper, wrapper_query
from sz_rpa1.rpa_add_new_user.log import get_driver_log
from sz_rpa1.rpa_add_new_user.main_func import close_window
from sz_rpa1.rpa_add_new_user.connect_mysql import update_data
from selenium.common.exceptions import NoAlertPresentException
from sz_rpa1.sz_rpa_batch_add.MyException import NoData, QueryErr
from sz_rpa1.rpa_add_new_user.connect_mysql import read_data
from sz_rpa1.sz_rpa_batch_add.MyException import NoData
from sz_rpa1.sz_rpa_batch_add.writedata_to_excel import write
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


@wrapper
def open_page(driver, file_name):
    # 参保管理
    cbgl = driver.find_element_by_id("returnYwsb('F02000')")
    cbgl.click()
    # 批量增加
    plzj = driver.find_element_by_id("grcbdjgl-p2")
    plzj.click()
    # 上传文件
    upload_file = driver.find_element_by_name("fileupload")
    upload_file.send_keys(file_name)


def main_func():
    # 登录
    url = 'https://sipub.sz.gov.cn/hsoms/logonDialog.jsp'
    driver = get_driver_log(url)
    # 关闭弹窗
    close_window(driver)
    sql = "select * from shenzhen_add where status in (0, 3)"
    data = read_data(sql)
    if not data:
        driver.close()
        try:
            raise NoData("数据库没有数据")
        except:
            logging = logging_fun()
            ret = traceback.format_exc()
            logging.error(ret)
            raise NoData("数据库没有数据")
    start = 0
    end = 50
    for _ in range((len(data)-1) // 50 + 1):
        data_list = data[start: end]
        start += 50
        end += 50
        file_name = write(data_list)
        try:
            input_info(driver, file_name, data_list)
        except QueryErr:
            # 记录异常日志
            logging = logging_fun()
            ret = traceback.format_exc()
            logging.error(ret)
        except NoData:
            # 记录异常日志
            logging = logging_fun()
            ret = traceback.format_exc()
            logging.error(ret)
        except:
            # time.sleep(2)
            driver.refresh()
            time.sleep(3)
            close_window(driver)
            time.sleep(2)
            try:
                input_info(driver, file_name, data_list)
            except QueryErr:
                # 记录异常日志
                logging = logging_fun()
                ret = traceback.format_exc()
                logging.error(ret)
            except NoData:
                # 记录异常日志
                logging = logging_fun()
                ret = traceback.format_exc()
                logging.error(ret)
            except:
                # 记录异常日志
                logging = logging_fun()
                ret = traceback.format_exc()
                logging.error(ret)
                # 申报失败的文件名存入该文件中
                pt = os.getcwd() + '/err_info'
                # print("提交失败的文件是%s" % file_name)
                with open('%s/not_submit_add_file.txt' % pt, 'a', encoding="utf-8") as f:
                    f.write("\n" + file_name)


def input_info(driver, file_name, data_list):
    # 打开页面, 输入文件
    open_page(driver, file_name)
    # 导入数据
    click_upload_file(driver, file_name)
    time.sleep(5)
    # 收集错误信息用户，修改数据库中内容， 然后再提交
    error_info_list = get_error_info_user(driver, file_name)
    # print(len(error_info_list), '错误用户', error_info_list)
    all_true_data = []
    for data in data_list:
        all_true_data.append(data[1])
    for info in error_info_list:
        all_true_data.remove(info[0])
        sql = "update shenzhen_add set status = 2, reason = '%s' where id_card = '%s'" % (info[1], info[0])
        update_data(sql)
    true_user_list = all_true_data
    # print('正确用户', true_user_list)
    # 申报作废
    # driver.find_element_by_name("btn_goAbort").click()
    # 申报提交
    sbtj = driver.find_element_by_name("btn_goNext")
    sbtj.click()
    # 如果正确的个数为0
    if not true_user_list:
        driver.switch_to_alert().accept()
        # 申报作废
        sbzf = driver.find_element_by_name("btn_goAbort")
        sbzf.click()
        raise NoData("提交时没数据")

    # 如果有错误信息
    if error_info_list:
        driver.switch_to_alert().accept()
    try:
        yd = driver.find_element_by_name("btn_goNext")
        yd.click()
    except:
        time.sleep(2)
        try:
            yd = driver.find_element_by_name("btn_goNext")
            yd.click()
        except:
            time.sleep(5)
            try:
                yd = driver.find_element_by_name("btn_goNext")
                yd.click()
            except:
                time.sleep(15)
                yd = driver.find_element_by_name("btn_goNext")
                yd.click()

    # 申报成功后关闭窗口
    # try:
    #     time.sleep(0.4)
    #     close_btn = driver.find_elements_by_class_name("dw-beacon-wnd-header-closebtn-ext")[1]
    #     close_btn.click()
    # except:
    #     time.sleep(2)
    #     close_btn = driver.find_elements_by_class_name("dw-beacon-wnd-header-closebtn-ext")[1]
    #     close_btn.click()
    # 改文件提交提交完成后去查询是否在系统里
    #      update_status(driver, true_user_list)
    # 信息录入完成后 开始查询
    # true_user_list = ["522725199310266155", '78999', '522725199310266155', '522725199310266157']
    try:
        update_status(driver, true_user_list, "shenzhen_add", "正常参保")
    # 查询异常后刷新一次继续查询
    except:
        driver.refresh()
        time.sleep(2)
        close_window(driver)
        try:
            update_status(driver, true_user_list, "shenzhen_add", "正常参保")
        except:
            pt = os.getcwd() + '/err_info'
            with open('%s/query_err_file.txt' % pt, 'a', encoding="utf-8") as f:
                f.write("\n" + file_name)
            raise QueryErr("查询时出错， 文件名为%s" % file_name)

# 填完信息后， 去查询确认在系统中
@wrapper_query
def update_status(driver, true_user_list, table_name, cb_status):
    open_info_query(driver)
    # 确认后的信息
    true_user_after_list = []
    # 异常用户
    query_no_info = []
    for id_card in true_user_list:
        ret = query_user_status(driver, id_card, cb_status)
        # print("ret", ret)
        if ret:
            sql = "update %s set status = 1, reason = '' where id_card = '%s'" % (table_name, id_card)
            update_data(sql)
            true_user_after_list.append(id_card)
        else:
            # 未查到信息
            sql = "update %s set status = 3, reason = '提交申报后未查到信息' where id_card = '%s'" % (table_name, id_card)
            update_data(sql)
            query_no_info.append(id_card)
    # print('query_no_info', query_no_info)
    # print('true_user_after_list', true_user_after_list)
    if len(true_user_after_list) > 1:
        sql = "update %s set status = 1 where id_card in %s" % (table_name, str(tuple(true_user_after_list)))
        update_data(sql)
    if len(true_user_after_list) == 1:
        sql = "update %s set status = 1 where id_card = '%s'" % (table_name, true_user_after_list[0])
        update_data(sql)


@wrapper_query
def open_info_query(driver):
    # 点开信息查询
    xxcx = driver.find_element_by_xpath('//div[@id="wsfw_nav"]/ul/li[2]')
    xxcx.click()
    time.sleep(0.5)
    # 员工信息查询
    ygxxcx = driver.find_elements_by_class_name('yjbt_mc')[1]
    ygxxcx.click()
    time.sleep(0.5)
    # 参保员工缴费信息
    cbjf = driver.find_element_by_xpath('//div[@id="wsfw_cont_left_xxcx"]/dl/dd[2]/ul/li[1]')
    cbjf.click()


@wrapper_query
def query_user_status(driver, id_card, cb_status):
    # 输入身份证
    zjhm = driver.find_element_by_name('yxzjhm')
    zjhm.clear()
    zjhm.send_keys(id_card)
    # 选择参保类型
    choose_zccb = driver.find_element_by_class_name('dw-sform-extdropdwon-lovbtn')
    choose_zccb.click()
    time.sleep(0.5)
    # 测试时用暂停参保
    zccb = driver.find_element_by_css_selector('div[title="%s"]' % cb_status)
    zccb.click()
    # 查询
    query = driver.find_element_by_name('btnQuery')
    query.click()
    time.sleep(1.5)
    # 获取当前文本内容的信息和输入的对比， 不正确或者为空则录入失败
    # 暂停参保用户
    query_result_element_list = driver.find_elements_by_xpath('//div[@class="datagrid-view2"]/div[2]/table/tbody/tr')
    if not query_result_element_list:
        time.sleep(2)
        query_result_element_list = driver.find_elements_by_xpath('//div[@class="datagrid-view2"]/div[2]/table/tbody/tr')
    if query_result_element_list:
        for query_result_element in query_result_element_list:
            # 姓名
            xm = query_result_element.find_element_by_xpath('./td[3]').text
            # 电脑号
            dnh = query_result_element.find_element_by_xpath('./td[4]').text
            # 身份证
            sfz = query_result_element.find_element_by_xpath('./td[6]').text
            print(xm, dnh, sfz)
            if id_card == sfz:
                return True
    # 为空或者不等于时返回False
    return False


@wrapper
def get_true_info(driver, *args):
    # 点击导入正确信息
    zqxx = driver.find_element_by_id("tab_truetab")
    zqxx.click()
    # 获取正确信息的人员
    obj = driver.find_element_by_xpath('//div[@class="datagrid-view1"]')
    el_list = obj.find_elements_by_xpath('./div[2]/table/tbody/tr')
    if not el_list:
        time.sleep(5)
        el_list = obj.find_elements_by_xpath('./div[2]/table/tbody/tr')
    true_info_list = []
    for el in el_list:
        one_true_info_list = []
        # 身份证/ 姓名/ 错误信息
        xm = el.find_element_by_xpath('./td[3]/div/div').text
        one_true_info_list.append(xm)
        sfz = el.find_element_by_xpath('./td[4]/div/div').text
        one_true_info_list.append(sfz)
        true_info_list.append(one_true_info_list)
    return true_info_list


@wrapper
def click_upload_file(driver, *args):
    # 导入数据
    try:
        drsj = driver.find_element_by_name("btnUpload")
        drsj.click()
        driver.switch_to_alert().accept()
        raise NoData("文件没数据")
    except NoAlertPresentException:
        pass


# 获取信息错误的用户
@wrapper
def get_error_info_user(driver, *args):
    # 点击错误信息
    cwxx = driver.find_element_by_id('tab_falsetab')
    cwxx.click()
    # 人员错误信息列表
    for _ in range(60):
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        ActionChains(driver).key_down(Keys.ARROW_DOWN).perform()
    error_info_list = []
    obj = driver.find_elements_by_xpath('//div[@class="datagrid-view2"]')[1]
    el_list = obj.find_elements_by_xpath('./div[2]/table/tbody/tr')

    if not el_list:
        time.sleep(2)
        el_list = obj.find_elements_by_xpath('./div[2]/table/tbody/tr')
    for el in el_list:
        one_error_info_list = []
        # 身份证/ 姓名/ 错误信息
        sfz = el.find_element_by_xpath('./td[2]/div/div').text
        one_error_info_list.append(sfz)
        # xm = el.find_element_by_xpath('./td[3]/div/div').text
        # one_error_info_list.append(xm)
        cwxx = el.find_element_by_xpath('./td[4]/div/div').text
        one_error_info_list.append(cwxx)
        # 批量修改时 只有一条数据的时候删除元组的，号
        error_info_list.append(one_error_info_list)
    return error_info_list


if __name__ == '__main__':
    try:
        main_func()
        time.sleep(10000)
    except NoData:
        print("数据库没数据")
