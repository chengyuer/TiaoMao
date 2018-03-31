#coding:utf-8
'''
做什么
'''

import  lxml
import lxml.etree

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0"
}

# filetext = open("fileseco.txt",'rb')
# text = filetext.read().decode('utf-8')
# mytree = lxml.etree.HTML(text)
#
# Jlist = mytree.xpath("//div[@id=\"J_ItemList\"]/div[@class=\"product item-1111 \"]")
# JlistLen = len(Jlist)
# print(JlistLen)
# Jlist = mytree.xpath("//div[@id=\"slogo-shopname\"]/ul/li[2]/a/text()")
# print(Jlist)
# JlistLen = len(Jlist)
# print(JlistLen)
#
filename = open("filepro.txt","rb")
text = filename.read().decode('utf-8')
mytree = lxml.etree.HTML(text)
Jlist = mytree.xpath("//a[@class=\"slogo-shopname\"]/strong/text()")
print(Jlist)
JlistLen = len(Jlist)
print(JlistLen)

# #
# for i in range(1,JlistLen + 1):
#     price = mytree.xpath("//div[@id=\"J_ItemList\"]/div[@class=\"product item-1111 \"][" + str(
#         i) + "]//p[@class=\"productPrice\"]/em/text()")[0]
#
#     # namelem = mytree.xpath("//div[@class=\"view grid-nosku view-noCom\"]/div[@class=\"product item-1111 \"][" + str(i) + "]//p[@class=\"productImg-wrap\"]/a[@class=\"productImg\"]")[0]
#     # print(namelem)
#     name = mytree.xpath("//div[@id=\"J_ItemList\"]/div[@class=\"product item-1111 \"]["+str(i                                                                                       )+"]//p[@class=\"productTitle\"]/a//@title")[0]
#
#
#     href = mytree.xpath("//div[@id=\"J_ItemList\"]/div[@class=\"product item-1111 \"]["+str(i)+"]//p[@class=\"productTitle\"]/a/@href")[0]
#
#     print(name, price ,href )
