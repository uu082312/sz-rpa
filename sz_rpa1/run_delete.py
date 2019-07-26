import sys,os
path_ab = os.path.abspath('..')
print(os.path.dirname('__file__'))
sys.path.append(path_ab)
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from sz_rpa1.sz_rpa_batch_delete.rpa_batch_delete import main_func
def my_job():
    print(datetime.datetime.now())
    main_func()
sched = BlockingScheduler()
sched.add_job(my_job, 'interval', max_instances=1, seconds=3)
sched.start()