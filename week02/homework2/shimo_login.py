"""
coding:utf8
@Time : 2020/8/1 22:47
@Author : cjr
@File : shimo_login.py
"""

from selenium import webdriver


try:
    browser = webdriver.Chrome()

    browser.get('https://shimo.im/login?from=home')
    btm1 = browser.find_element_by_xpath(
        '//*[@id="root"]/div/div[2]/div/div/div/div[2]/div/div/div[1]/div[1]/div/input'
    ).send_keys('18104620243')
    btm2 = browser.find_element_by_xpath(
        '//*[@id="root"]/div/div[2]/div/div/div/div[2]/div/div/div[1]/div[2]/div/input'
    ).send_keys('wawy5211314')

    browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div/div/div[2]/div/div/div[1]/button').click()

    cookies = browser.get_cookies()

    print(cookies)


except Exception as e:
    print(e)
finally:
    browser.close()




