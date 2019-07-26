# --coding: utf-8 --
import xlwt
import uuid
import os
from sz_rpa1.rpa_add_new_user.connect_mysql import read_data
from sz_rpa1.sz_rpa_batch_delete.MyException import NoData


def write(data_list):
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('sheet1')
    info_name_list = ['社会保障号码', '姓名', '是否本人意愿']
    for index, info in enumerate(info_name_list):
        worksheet.write(0, index, label=info)
    for hang, user_info in enumerate(data_list, 1):
        for lie, user in enumerate(user_info[1: -3]):
            if user == "None":
                user = ""
            worksheet.write(hang, lie, label=str(user))
    file_path =os.path.dirname(__file__) + r'/excel_file/delete-%s.xls' % uuid.uuid4()
    workbook.save(file_path)
    return file_path
