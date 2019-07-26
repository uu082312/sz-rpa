# coding: utf-8
import sys,os
path_ab = os.path.abspath('..')
path_ab_parent = os.path.abspath('../../')
print(os.path.dirname('__file__'))
sys.path.append(path_ab)
sys.path.append(path_ab_parent)
import time
from sz_rpa1.sz_rpa_batch_delete.rpa_batch_delete import main_func


if __name__ == '__main__':
    main_func()
    print("执行完成")
    # time.sleep(10000)

