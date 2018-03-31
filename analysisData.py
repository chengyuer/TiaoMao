#coding:utf-8
'''
对店铺用户评论进行情感分析
情感分析结果大多为负面 分数1  无奈··
'''
import os

import time
from aip import AipNlp

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0"
}


""" 你的 APPID AK SK """
APP_ID = '10254547'
API_KEY = 'KN3hFlvWrHykUD8iN12Ah8Q1'
SECRET_KEY = 'pPhhSxEnuKa30nUIj2elReioqLMsHolw '
aipNlp = AipNlp(APP_ID, API_KEY, SECRET_KEY)



# 递归得到一个项目下的所有文件夹
def getFile(mpath):
    if (os.path.exists(mpath)):
        files = os.listdir(mpath)
        filelist = []
        filepath = mpath + "/"
        for mfile in files:
            if (os.path.isfile(filepath +mfile) and mfile.find("txt") != -1):
                filelist.append(filepath +mfile)
            elif os.path.isdir(filepath +mfile):
                # print(filepath+mfile)
                filelist += getFile(filepath + mfile)
            else:
                pass
        for f in filelist:
            print(f)
        print(len(filelist))
        return filelist

if __name__ == '__main__':

    files = getFile("files")
    mfile = open('result.txt','wb')
    for file in files:
        commentscore = 0
        commentstr = open(file,"rb").read().decode('utf-8')
        # print(file)
        # print(commentstr)
        print("********************************************8")
        result = aipNlp.sentimentClassify(commentstr)
        try:
            commentscore += result['items'][0]['sentiment']
        except :
            commentscore = 0
        print(commentscore)
        time.sleep(2)
        name = file.replace('/', " ").replace("files", "").replace(".txt", "")
        if commentscore > 6:
            print(name, "情感分析：正面", "分数：", str(commentscore))
            mfile.write(
                (name +  "情感分析：正面"+ "分数："+ str(commentscore)).encode('utf-8'))
            mfile.flush()
        if commentscore== 5 or commentscore == 6:
            print(name, "情感分析：中性", "分数：", str(commentscore))
            mfile.write(
                (name+ " " + "情感分析：中性" + " " + "分数：" + str(commentscore) + "\r\n").encode("utf-8", "ignore"))
            mfile.flush()
        if commentscore <= 4:
            print(name , "情感分析：负面", "分数：", str(commentscore))
            mfile.write(
                (name+ " " + "情感分析：负面" + " " + "分数：" + str(commentscore) + "\r\n").encode("utf-8", "ignore"))
            mfile.flush()
        time.sleep(1)
