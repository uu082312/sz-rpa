import logging
import os


def logging_fun():
    pt = os.getcwd() + '/err_info'
    logging.basicConfig(filename='%s/rpa.log' % pt,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(module)s: %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=40)
    return logging
