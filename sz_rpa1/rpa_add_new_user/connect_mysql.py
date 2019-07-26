# coding: utf-8
import pymysql


def read_data(sql):
    db = pymysql.connect(host='172.16.14.23', port=3306, user='db3', password='Lps!@#123', db='shebaoRPA', charset='utf8')
    cursor = db.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    db.close()
    return data


def update_data(sql):
    db = pymysql.connect(host='172.16.14.23', port=3306, user='db3', password='Lps!@#123', db='shebaoRPA', charset='utf8')
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()
    cursor.close()
    db.close()
    return 'ok'


# def insert_data(sql):



if __name__ == '__main__':
    # sql = "select * from shenzhen_add"
    # read_data(sql)
    # true_user_after_list = ['522725199310266155', '522725199310266156']
    # sql = "update sz_input_info set status = 1 where id_card in %s" % str(tuple(true_user_after_list))
    # sql = "update shenzhen_add set status = 3, reason = '查不到信息' where id_card = '522725199310266155'"
    # sql = "update sz_input_info set status = 1 where id_card = '522725199310266155'"
    file_name = "C:/Users/andap/Desktop/batchadd-c8741442-cbff-412a-82ee-dd6dea02f08c.xls"
    sql = "select err_num from shenzhen_file where file_name = '%s'" % file_name
    ret = read_data(sql)[0][0]
    print(ret, type(ret))
    print('修改完成')
