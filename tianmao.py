#coding:utf-8
'''
登录天猫  ，搜索小米wifi，检索综合排名前60的热门小米产品  挖掘用户评价，并对评价进行情感分析
'''
import time

import lxml
import lxml.etree
import os
import selenium
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities, ActionChains
from selenium.webdriver.common.keys import Keys#鼠标动作

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0"
}

url = "https://login.tmall.com/"

if __name__ == '__main__':

    # 打开火狐浏览器
    driver = webdriver.Firefox()
    driver.get(url)
    time.sleep(2)

    iframe = driver.find_element_by_id("J_loginIframe")
    driver.switch_to_frame(iframe)

    try:
        elem = driver.find_element_by_link_text('密码登录')
        elem.click()
        time.sleep(2)
    except Exception as e:
        print(e)
        pass

    # 模拟输入账号密码
    username = driver.find_element_by_id("TPL_username_1")
    password = driver.find_element_by_id("TPL_password_1")
    username.send_keys("18370802679")
    time.sleep(2)
    password.send_keys("alterpasswordagain")
    time.sleep(2)
    click = driver.find_element_by_id("J_SubmitStatic")
    # 点击登录按钮，登录成功
    click.click()
    time.sleep(20)


    driver.switch_to_default_content()#切回主文档

    time.sleep(0.5)
    mqelem = driver.find_element_by_name("q")
    # mqelem = driver.find_element_by_class_name("s-combobox-input")
    mqelem.send_keys("小米WiFi")
    mqelem.send_keys(Keys.RETURN)#执行回车键
    time.sleep(10)

    pagesource = driver.page_source
    mytree = lxml.etree.HTML(pagesource)
    Jlist = mytree.xpath("//div[@id=\"J_ItemList\"]/div[@class=\"product item-1111 \"]")
    JlistLen = len(Jlist)
    print(JlistLen)
    filename = open("product.txt","wb")
    hreflist = []
    productlist = []
    # try:
    for i in range(1,JlistLen + 1):
        print("翻页",str(i))
        time.sleep(8)
        pagesource = driver.page_source
        mytree = lxml.etree.HTML(pagesource)
        try:
            price = mytree.xpath("//div[@id=\"J_ItemList\"]/div[@class=\"product item-1111 \"][" + str(
                i) + "]//p[@class=\"productPrice\"]/em/text()")[0]

        except  Exception as e:
            print("price"  , e)
            price = "no"


        try:
            name = mytree.xpath("//div[@class=\"view grid-nosku view-noCom\"]/div[@class=\"product item-1111 \"][" + str(
                i) + "]//p[@class=\"productTitle\"]/a/@title")[0]
        except Exception as e:
            print("name", e)
            name = "no"

        try:
            href = mytree.xpath("//div[@id=\"J_ItemList\"]/div[@class=\"product item-1111 \"][" + str(
                i) + "]//p[@class=\"productTitle\"]/a/@href")[0]

        except Exception  as e:
            print("href" , e)
            href = "no"
        print(name, price ,href )

        js = "var q=document.documentElement.scrollTop=300"#页面滚动
        driver.execute_script(js)#执行js
        time.sleep(3)
        namelem = driver.find_element_by_xpath("//div[@class=\"view grid-nosku view-noCom\"]/div[@class=\"product item-1111 \"][" + str(
                i) + "]//div[@class=\"productImg-wrap\"]/a[@class=\"productImg\"]")
        print(namelem)
        # namelem = driver.find_element_by_class_name("productImg")
        ActionChains(driver).move_to_element(namelem).perform()
        time.sleep(0.5)
        namelem.click()  # 点击商品名称
        time.sleep(5)
        print("点击商品切换窗口")

        firstwin = driver.current_window_handle  # 当前的窗体
        allwindows = driver.window_handles  # 所有的窗口
        print("所有窗体长度",str(len(allwindows)))
        # 选择注册窗口
        for win in allwindows:
            if win != firstwin:
                driver.switch_to.window(win)
                print("切换成功")
                time.sleep(5)
                driver.switch_to_default_content()
                time.sleep(17)
                # 切换为新打开的页面
                try:
                    # 将页面滚动条拖到商品评论处
                    for j in range(1, 2):
                        # js = "document.body.scrollTop=" + str(3000 * i)
                        js = "var q=document.documentElement.scrollTop=" + str(1500 * j)
                        driver.execute_script(js)
                        time.sleep(3)
                except Exception as e:
                    print("滚动条错误", e)



                mytree = lxml.etree.HTML(driver.page_source)

                fname = mytree.xpath("//a[@class=\"slogo-shopname\"]/strong/text()")[0] if (
                    len(mytree.xpath("//a[@class=\"slogo-shopname\"]/strong/text()")) != 0) else "店铺无名"
                print(fname)
                filetext = "files/"+fname
                if(os.path.exists(filetext)):
                    pass
                else:
                    os.makedirs(filetext)

                filecomment = open(filetext +"/" + name.replace("/","") + ".txt", 'wb')
                productinfo = name + " " + price + " " + href
                print(productinfo)

                try:
                    # elem = driver.find_element_by_xpath("//div[@id=\"J_TabBarBox\"]/ul/li[2]/a")
                    # elem = driver.find_element_by_link_text("累计评价")
                    elem = driver.find_element_by_xpath("//em[@class=\"J_ReviewsCount\"]")
                    ActionChains(driver).move_to_element(elem).perform()
                    time.sleep(0.5)
                    elem.click()  # 点击商品评论
                    time.sleep(15)

                except Exception as e:
                    print("点击商品评论错误", e)
                try:

                    # 发现评论
                    print("发现评论")
                    for k in range(1, 3):
                        js = "var q=document.documentElement.scrollTop=4000"
                        driver.execute_script(js)
                        time.sleep(3)
                        # js = "document.body.scrollTop=" + str(2000 * i)
                        js = "var q=document.documentElement.scrollTop=" + str(2000 * k)
                        driver.execute_script(js)
                        time.sleep(5)

                    html = driver.page_source
                    mytree = lxml.etree.HTML(html)

                    filecomment.write((productinfo + "\r\n" + "\r\n").encode('utf-8'))
                    for m in range(10):
                        html = driver.page_source
                        mytree = lxml.etree.HTML(html)
                        commentlist = mytree.xpath("//div[@class=\"rate-grid\"]//tr")
                        if(len(commentlist) ==0):
                            break

                        for d in range(1, len(commentlist) + 1):
                            commentinit = mytree.xpath(
                                "//div[@class=\"rate-grid\"]//tr[" + str(
                                    d) + "]//div[@class=\"tm-rate-fulltxt\"]/text()")
                            mstr = ""
                            for o in range(len(commentinit)):
                                mstr = mstr + commentinit[o] + ","

                            filecomment.write((mstr + "\r\n" + "\r\n").encode('utf-8'))
                            print("********************")
                            print(commentinit)

                        count = 1
                        distance = 500
                        while True:
                            try:
                                nextpage = driver.find_element_by_link_text("下一页>>")
                                ActionChains(driver).move_to_element(nextpage).perform()
                                time.sleep(0.5)
                                nextpage.click()  # 点击下一页
                                time.sleep(7)
                                break
                            except :
                                js = "var q=document.documentElement.scrollTop="+str(count*distance)
                                driver.execute_script(js)
                                count += 1
                                time.sleep(1.5)
                                if(count > 20):
                                    count = 1
                                    distance = distance -100



                    filecomment.close()
                    driver.close()
                    driver.switch_to_window(allwindows[0])

                except  Exception as e:
                    print("发现评论错误", e)
                    driver.close()
                    driver.switch_to_window(allwindows[0])




    filename.close()








