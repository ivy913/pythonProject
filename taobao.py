from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime
import requests

#定义一个taobao类
class taobao_infos:
    #对象初始化
    def __init__(self):
        url='https://login.taobao.com/member/login.jhtml'
        self.url=url
        options=webdriver.ChromeOptions() #配置 chrome 启动属性
        #options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2}) #不加载图片，加快访问速度
        options.add_experimental_option("excludeSwitches",['enable-automation']) # 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium
        self.browser=webdriver.Chrome(options=options)
        self.wait=WebDriverWait(self.browser, 10, 0.1) #超时时长为10s

    #扫码登陆淘宝
    def login(self):
        #打开网页
        self.browser.get(self.url)
        time.sleep(10)

    #打开抢购商品首页
    def get_shop(self,shop_url,buytime):
        print("正在打开需要抢购的页面")
        self.browser.get(shop_url)
        while True:
            if time_server() >= datetime.strptime(buytime, "%Y-%m-%d %H:%M:%S"):
                try:
                    color=self.wait.until(EC.presence_of_element_located((By.XPATH, '//ul[@class="tm-clear J_TSaleProp tb-img     "]/li[1]/a')))
                    color.click()
                    print("已选择颜色分类1")
                    num=self.wait.until(EC.presence_of_element_located((By.XPATH, '//span[@class="mui-amount-increase"]')))
                    num.click()
                    print("已选择数量2")
                    #等待购买按钮出现
                    div=WebDriverWait(self.browser).until(EC.visibility_of_element_located((By.XPATH,"//div[@class='tb-action tm-clear']")))
                    print("可点击下单")
                    linkbuy=self.wait.until(EC.presence_of_element_located((By.ID, 'J_LinkBuy')))
                    linkbuy.click()
                    print("已点击下单")
                    sutj=self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="wrapper"]/a')))
                    sutj.click()
                    print(f"抢购成功，请尽快付款")
                except Exception as e:
                    print("出现如下异常%s"%e)
                    self.browser.refresh()  # 刷新页面
                    div=WebDriverWait(self.browser).until(EC.visibility_of_element_located((By.xpath,"//div[@class='tb-action tm-clear']")))
                    linkbuy = self.wait.until(EC.presence_of_element_located((By.ID, 'J_LinkBuy')))
                    linkbuy.click()
                    sutj = self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="wrapper"]/a')))
                    sutj.click()
                    print(f"抢购成功，请尽快付款")

    def gb(self):
        print(">>> 抢购完毕，关闭浏览器！")
        self.browser.quit()


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


if __name__ == '__main__':
    spider = taobao_infos()
    spider.login()
    buytime = '2020-03-02 11:59:58'
    shop_url = "https://chaoshi.detail.tmall.com/item.htm?spm=a1z0d.6639537.1997196601.3.5a097484aOFCTv&id=20739895092"
    try:
        spider.get_shop(shop_url, buytime)
    except:
        spider.get_shop(shop_url, buytime)
    spider.gb()
