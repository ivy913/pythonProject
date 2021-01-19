from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import requests
from datetime import datetime

# 输入秒杀时间
start_time = "2021-1-18 20:00:00"
password = "520913"
print("你只有15秒的登录时间")
# 将输入的时间进行格式化
timeArray = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
# 用来判断 你是订单提交失败还是支付失败
sum = 0
# 设置chrome驱动的路径
driver = webdriver.Chrome()
# 打开淘宝的登录界面
driver.get("https://cart.taobao.com/cart.htm")
# 最大化浏览器
# driver.maximize_window()

# 判断全选框是否出现 出现则点击全选 否则继续等待 最多等待15秒
try:
    WebDriverWait(driver, 15, 0.1).until(
        lambda el: driver.find_element_by_xpath('//*[@id="J_SelectAll1"]/div/label')).click()
except:
    print("登录失败")


def time_server():
    # 获取淘宝服务器的时间戳
    r1 = requests.get(url='http://api.m.taobao.com/rest/api3.do?api=mtop.common.getTimestamp',
                      headers={
                          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.4098.3 Safari/537.36'}
                      ).json()['data']['t']
    # 把时间戳格式/1000 获取毫秒
    timeNum = int(r1) / 1000
    # 格式化时间 (小数点后6为)
    time1 = datetime.fromtimestamp(timeNum)
    return time1


# 等待时间到预定的时间
print("等待中")

while True:
    # 判断时间服务器时间是否大于或等于输入的时间
    if time_server() >= timeArray:
        # 点击结算
        print("淘宝时间：",time_server(),"，开始结算")
        driver.find_element_by_xpath('//*[@id="J_Go"]').click()
        break
    else:
        continue

try:
    # 判断提交订单的按钮是否出现 出现就点击 否则继续等待 最多等待5秒
    WebDriverWait(driver, 5, 0.01).until(
        lambda el: driver.find_element_by_xpath('//*[@id="submitOrderPC_1"]/div/a[2]')).click()
    print("订单提交成功")
    print("秒杀成功")
    sum = 1
    # 判断输入密码的框是否出现 出现就输入密码
    WebDriverWait(driver, 5, 0.01).until(
        lambda el: driver.find_element_by_xpath('//*[@id="submitOrderPC_1"]/div/a[2]')).send_keys(password)
    # 点击确认付款
    driver.find_element_by_xpath('//*[@id="J_authSubmit"]').click()
    print("付款成功")
except Exception as e:
    print("出现如下异常%s"%e)
    if sum == 0:
        print("提交订单失败")
    else:
        print("付款失败")
