# coding: utf-8
import time


def wrapper(fun):
    def inner(driver, *args):
        try:
            time.sleep(0.5)
            err_user = fun(driver, *args)
            return err_user
        except:
            time.sleep(5)
            err_user = fun(driver, *args)
            return err_user

    return inner


def wrapper_open_page(fun):
    def inner(driver, file_name, *args):
        try:
            time.sleep(0.5)
            err_user = fun(driver, file_name, *args)
            return err_user
        except:
            time.sleep(5)
            err_user = fun(driver, file_name, *args)
            return err_user

    return inner


