import json
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

class TestCookie:
    def setup(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://work.weixin.qq.com/wework_admin/loginpage_wx")

    def test_cookie(self):
        sleep(15)#强制等待15s
        #将获取到的cookie 存放到json文件中，不需要格式转换
        cookies = self.driver.get_cookies()
        with open("cookie_wechat.json","w")as f:
            json.dump(cookies,f)

    def test_cookie_login(self):
        cookies = json.load(open('cookie_wechat.json'))
        for cookie in cookies:
            self.driver.add_cookie(cookie)
        while True:
            self.driver.refresh()#刷新
            r = WebDriverWait(self.driver,10).until(expected_conditions.element_to_be_clickable((By.ID, "menu_index")))
            if r is not True:
                break
        # expected_conditions.xx 都需要传入的是一个元祖
        # 定位并点击通讯录
        WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable
                                             ((By.CSS_SELECTOR, ".index_service_cnt_itemWrap:nth-child(2)"))).click()
        # send_keys需要使用绝对路径
        # send_keys上传文件,使用绝对路径
        self.driver.find_element(By.ID, "js_upload_file_input"). \
            send_keys(r"E:\python_pytest\test_selenium\workbook.xlsx")

        WebDriverWait(self.driver, 10).until(
            expected_conditions.presence_of_element_located((By.ID, "upload_file_name")))

        # 断言是否是workbook.xlsx相等
        assert_ele = self.driver.find_element(By.ID, "upload_file_name").text

    def teardown(self):
        self.driver.quit()