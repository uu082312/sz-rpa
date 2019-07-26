# --coding: utf-8 --
import time


def wrapper(fun):
    def inner(driver, file_name, *args):
        try:
            time.sleep(0.5)
            status = fun(driver, file_name, *args)
            return status
        except:
            time.sleep(5)
            try:
                status = fun(driver, file_name,  *args)
                return status
            except:
                time.sleep(9)
                try:
                    status = fun(driver, file_name, *args)
                    return status
                except:
                    time.sleep(10)
                    status = fun(driver, file_name, *args)
                    return status

    return inner


def wrapper_query(func):
    def inner(driver, *args):
        try:
            time.sleep(0.5)
            ret = func(driver, *args)
            return ret
        except:
            time.sleep(3)
            ret = func(driver, *args)
            return ret

    return inner
