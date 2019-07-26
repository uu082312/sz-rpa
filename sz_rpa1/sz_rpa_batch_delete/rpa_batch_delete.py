# --coding: utf-8 --
import time
import os
import traceback
from sz_rpa1.rpa_add_new_user.log import get_driver_log
from sz_rpa1.rpa_add_new_user.main_func import close_window
from sz_rpa1.sz_rpa_batch_delete.delayed import wrapper, wrapper_open_page
from selenium.common.exceptions import NoAlertPresentException
from sz_rpa1.sz_rpa_batch_delete.MyException import NoData
from sz_rpa1.rpa_add_new_user.connect_mysql import update_data
from sz_rpa1.rpa_add_new_user.rpa_logging import logging_fun
from sz_rpa1.sz_rpa_batch_add.batch_add import update_status
from sz_rpa1.sz_rpa_batch_add.MyException import QueryErr
from selenium.webdriver.common.action_chains import ActionChains #引入鼠标
from selenium.webdriver.common.keys import Keys #引入键盘
from sz_rpa1.rpa_add_new_user.connect_mysql import read_data
from sz_rpa1.sz_rpa_batch_delete.writedata_to_excel import write


def main_func():
    # 登录
    url = 'https://sipub.sz.gov.cn/hsoms/logonDialog.jsp'
    driver = get_driver_log(url)
    # 关闭弹窗
    close_window(driver)
    # file_path_list = paging()
    # for file_path in file_path_list:
    sql = "select * from shenzhen_less where status=0"
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
    # 文件路径列表，1---》
    # file_path_list = []
    for _ in range((len(data)-1) // 50 + 1):
        data_list = data[start: end]
        start += 50
        end += 50
        file_path = write(data_list)
        # print('data_list', data_list)
        # time.sleep(10000)
        try:
            input_info(driver, file_path, data_list)
        except QueryErr:
            # 记录异常日志
            logging = logging_fun()
            ret = traceback.format_exc()
            logging.error(ret)
        except:
            driver.refresh()
            time.sleep(4)
            close_window(driver)
            time.sleep(2)
            try:
                input_info(driver, file_path, data_list)
            except QueryErr:
                # 记录异常日志
                logging = logging_fun()
                ret = traceback.format_exc()
                logging.error(ret)
            except:
                pt = os.getcwd() + '/err_info'
                with open('%s/not_submit_del_file.txt' % pt, 'a', encoding="utf-8") as f:
                    f.write("\n" + file_path)
                # 记录异常日志
                logging = logging_fun()
                ret = traceback.format_exc()
                logging.error(ret)


@wrapper_open_page
def input_info(driver, file_name, data_list):
    # 参保管理
    cbgl = driver.find_element_by_id("returnYwsb('F02000')")
    cbgl.click()
    # 批量减员
    pljy = driver.find_element_by_id("grcbdjgl-p4")
    pljy.click()
    # 报表文件
    file = driver.find_elements_by_class_name("xzywblms_li")[1]
    file.click()
    next_step = driver.find_element_by_name("btn_goNext")
    next_step.click()
    time.sleep(0.5)
    # 上传文件
    upload_file = driver.find_element_by_name("fileupload")
    upload_file.send_keys(file_name)
    # 导入数据, 没有数据出现弹窗
    try:
        up_data = driver.find_element_by_name("btnUpload")
        up_data.click()
        driver.switch_to_alert().accept()
        raise NoData("导入文件没数据")
    except NoAlertPresentException:
        # 收集错误信息
        err_list = get_err_user(driver)
        # print(len(err_list), "错误个数", err_list)
        # 一个文件的所有正确信息
        all_true_data = []
        for data in data_list:
            all_true_data.append(data[1])
        for err in err_list:
            all_true_data.remove(err[0])
            sql = "update shenzhen_less set status = 2, reason = '%s' where id_card = '%s'" % (err[2], err[0])
            update_data(sql)
        # print('all_true_data', all_true_data)
        # 收集正确信息， 去暂停参保查询
        true_user_list = all_true_data
        # 点击申报作废
        # driver.find_element_by_name("btn_goAbort").click()
        # driver.switch_to_alert().accept()
        # time.sleep(1)
        # 信息录入完成后 开始查询
        # true_user_list = ["522725199310266155", '78999', '522725199310266155', '522725199310266157']
        # 申报提交
        sbtj = driver.find_element_by_name("btn_goNext")
        sbtj.click()
        # 提交没数据
        if not true_user_list:
            time.sleep(0.5)
            driver.switch_to_alert().accept()
            # 申报作废
            sbzf = driver.find_element_by_name("btn_goAbort")
            sbzf.click()
            raise NoData("提交时没数据")
        # 有错误信息
        if err_list:
            time.sleep(0.5)
            driver.switch_to_alert().accept()
        # 申报提交
        # try:
        #     sbtj = driver.find_element_by_name("btn_goNext")
        #     sbtj.click()
        #     time.sleep(0.2)
        #     driver.switch_to_alert().accept()
        #     raise NoData("提交时没数据")
        # except NoAlertPresentException:
        #     pass
            # print("点击申报成功")
        # 申报成功后关闭窗口
        try:
            time.sleep(0.4)
            # close_btn = driver.find_elements_by_class_name("dw-beacon-wnd-header-closebtn-ext")[1]
            close_btn = driver.find_element_by_name("btn_goNext")
            close_btn.click()
        except:
            time.sleep(2)
            try:
                close_btn = driver.find_element_by_name("btn_goNext")
                close_btn.click()
            except:
                time.sleep(5)
                close_btn = driver.find_element_by_name("btn_goNext")
                close_btn.click()
        try:
            update_status(driver, true_user_list, "shenzhen_less", "暂停参保")
        # # 查询异常后刷新一次继续查询
        except:
            driver.refresh()
            time.sleep(2)
            close_window(driver)
            try:
                update_status(driver, true_user_list, "shenzhen_less", "暂停参保")
            except:
                pt = os.getcwd() + '/err_info'
                with open('%s/query_err_file.txt' % pt, 'a', encoding="utf-8") as f:
                    f.write("\n" + file_name)
                raise QueryErr("查询时出错， 文件名为%s" % file_name)

# 错误信息
@wrapper
def get_err_user(driver):
    err_info = driver.find_element_by_id("tab_falsetab")
    err_info.click()
    # time.sleep(2)
    for i in range(100):
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        ActionChains(driver).key_down(Keys.ARROW_DOWN).perform()
        # print(i)
        # time.sleep(0.5)

    err_obj = driver.find_elements_by_class_name("datagrid-view2")[1]
    err_info_element_list = err_obj.find_elements_by_xpath("./div[2]/table/tbody/tr")
    time.sleep(1)
    # print("err_info_element_list", len(err_info_element_list))
    if not err_info_element_list:
        time.sleep(2)
        err_info_element_list = err_obj.find_elements_by_xpath("./div[2]/table/tbody/tr")
    err_info_user_list = []
    for err_info_element in err_info_element_list:
        err_info_user = []
        sfz = err_info_element.find_element_by_xpath("./td[2]/div/div").text
        err_info_user.append(sfz)
        xm = err_info_element.find_element_by_xpath("./td[3]/div/div").text
        err_info_user.append(xm)
        cwxx = err_info_element.find_element_by_xpath("./td[4]/div/div").text
        err_info_user.append(cwxx)
        err_info_user_list.append(tuple(err_info_user))

    return err_info_user_list


@wrapper
def get_true_user(driver):
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
        # 身份证/ 姓名
        xm = el.find_element_by_xpath('./td[3]/div/div').text
        one_true_info_list.append(xm)
        sfz = el.find_element_by_xpath('./td[4]/div/div').text
        one_true_info_list.append(sfz)
        true_info_list.append(one_true_info_list)
    return true_info_list


if __name__ == '__main__':
    main_func()
