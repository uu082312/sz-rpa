# --coding: utf-8 --
import xlwt
import os
import uuid


def write(data_list):
    info_name_list = ['证件号码', '姓名', '户籍', '入深户时间', '民族', '手机号码', '通讯地址', '岗位类别', '个人身份', '用工形式', '学历', '医疗缴费档次', '缴费工资',
                      '部门名称']
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('sheet1')
    for index, info in enumerate(info_name_list):
        worksheet.write(0, index, label=info)
    for hang, user_info in enumerate(data_list, 1):
        for lie, user in enumerate(user_info[1: -3]):
            if not user:
                user = ""
            worksheet.write(hang, lie, label=str(user))
    path = os.path.dirname(__file__)
    file_path = path + '/excel_file/batchadd-%s.xls' % uuid.uuid4()
    workbook.save(file_path)
    return file_path


