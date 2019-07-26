import time
import traceback
from selenium.common.exceptions import NoSuchElementException
from sz_rpa1.rpa_add_new_user.rpa_logging import logging_fun
from sz_rpa1.rpa_add_new_user.connect_mysql import read_data, update_data

user_info = ''


class ErrorUser(Exception):
    pass


class ErrorPage(Exception):
    pass


def wrapper_commit_ago(fun):
    def inner(driver, name, *args):
        try:
            time.sleep(0.2)
            if name == "cszjhm":
                global user_info
                user_info = args[0]
            fun(driver, name, *args)
        except NoSuchElementException:
            print('NoSuchElementException异常')
            # 记录异常日志
            logging = logging_fun()
            ret = traceback.format_exc()
            logging.error(ret)
            time.sleep(2)
            try:
                fun(driver, name, *args)
            except:
                # 记录异常日志
                logging = logging_fun()
                ret = traceback.format_exc()
                logging.error(ret)
                # 重新增加用户
                from sz_rpa1.rpa_add_new_user.main_func import open_info_page, close_window, write_info
                query_sql = "select err_num from shenzhen_add where identity_no = '%s'" % user_info
                err_num = read_data(query_sql)[0][0]
                if err_num < 3:
                    err_num += 1
                    # 修改数据库中的错误次数
                    update_sql = "update shenzhen_add set err_num = %s where identity_no = '%s'" % (err_num, user_info)
                    update_data(update_sql)
                    driver.refresh()
                    time.sleep(3)
                    close_window(driver)
                    info_sql = "select * from shenzhen_add where identity_no = '%s'" % user_info
                    info = read_data(info_sql)[0]
                    open_info_page(driver, info)
                    # write_info(driver, info)
                else:
                    # 重新填写三次后还是失败， 直接跳过该用户
                    raise ErrorPage("错误页面")

    return inner


def wrapper_open_page(fun):
    def inner(driver, name, *args):
        try:
            time.sleep(0.3)
            fun(driver, name, *args)
        except NoSuchElementException:
            time.sleep(2)
            try:
                fun(driver, name, *args)
            except:
                driver.refresh()
                time.sleep(3)
                from sz_rpa1.sz_rpa_batch_add.batch_add import open_page
                # 关闭弹窗, 打开信息页面
                open_page(driver)

    return inner
