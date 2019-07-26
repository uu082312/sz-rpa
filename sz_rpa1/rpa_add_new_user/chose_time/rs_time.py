import time
from sz_rpa1.sz_rpa_batch_add.get_element import get_element_by_id_send, get_element_by_id_click


def chose_time(min_time, driver, y, m, d):
    # 获取点开时年份的第一个年份标签对象
    y_obj = driver.find_element_by_xpath('//ul[@id="laydate_ys"]//li[1]')
    # 点开年份时第一个数据对应的年
    first_year = int(y_obj.text[0:-1])
    # first_year = int(first_yea)
    # 比他大，上翻
    if first_year > min_time:
        # 翻页次数
        num = (first_year - min_time) // 14
        top = driver.find_element_by_class_name("laydate_chtop")
        for _ in range(num):
            time.sleep(0.1)
            top.click()
        chose_year = driver.find_element_by_css_selector('li[y="%d"]' % y)
        chose_year.click()
        # time.sleep(0.5)
        # 点开月份
        get_element_by_id_click(driver, "laydate_m")
        time.sleep(0.1)
        chose_month = driver.find_element_by_css_selector('span[m="%d"]' % (m - 1))
        chose_month.click()
        time.sleep(0.1)
        chose_day = driver.find_element_by_css_selector('td[y="%d"][m="%d"][d="%d"]' % (y, m, d))
        chose_day.click()
    else:
        num = (min_time - first_year) // 14
        down = driver.find_element_by_class_name('laydate_chdown')
        for _ in range(num):
            time.sleep(0.1)
            down.click()
        # 通过传入的年选择年份，点击
        chose_year = driver.find_element_by_css_selector('li[y="%d"]' % y)
        chose_year.click()
        time.sleep(0.2)
        # 点开月份
        get_element_by_id_click(driver, "laydate_m")
        time.sleep(0.2)
        chose_month = driver.find_element_by_css_selector('span[m="%d"]' % (m - 1))
        chose_month.click()
        time.sleep(0.2)
        chose_day = driver.find_element_by_css_selector('td[y="%d"][m="%d"][d="%d"]' % (y, m, d))
        chose_day.click()