#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import requests
from mysql.mySqlUtil import DBHelper

class QSBK:

    # 初始化方法，定义一些变量
    def __init__(self):
        #页码
        self.pageIndex = 1
        #最大页数
        self.maxPage = 13
        # 反链
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        # 初始化 headers
        self.headers = {'User-Agent': self.user_agent}
        # 存放段子，每一个元素是每一页的段子们
        self.stories = []

    # 传入某一页的索引获得页面代码
    def getPage(self, pageIndex):
        try:
            url = 'http://www.qiushibaike.com/hot/page/' + str(pageIndex)
            # 构建请求的 request
            request = requests.get(url, headers=self.headers)
            return request.content.decode('utf-8')

        except requests.exceptions as e:
            if hasattr(e, "reason"):
                print(u"连接糗事百科失败, 错误原因", e.reason)
                return None

    # 传入某一页代码，返回本页不带图片的段子列表
    def getPageItems(self, pageIndex):
        pageCode = self.getPage(pageIndex)
        if not pageCode:
            print("页面加载失败....")
            return None
        pattern = re.compile(
            '<div class="author clearfix">.*?<a.*?<h2>(.*?)</h2>.*?<div class="articleGender manIcon">(.*?)</div>.*?<div class="content">.*?<span>(.*?)</span>.*?<span class="stats-vote"><i class="number">(.*?)</i>',
            re.S)
        items = re.findall(pattern, pageCode)

        # author = re.findall(r'<div class="author clearfix">.*?<h2>(.*?)</h2>', pageCode, re.S)
        # # lv = re.findall(r'<div class="articleGender manIcon">(.*?)</div>', pageCode, re.S)
        # content = re.findall(r'<div class="content">.*?<span>(.*?)</span>', pageCode, re.S)
        # zan = re.findall(r'<span class="stats-vote"><i class="number">(.*?)</i>', pageCode, re.S)

        # 用来存储每页的段子们
        pageStories = []
        # pageStories = [author, content, 0, zan]
        # 遍历正则表达式匹配的信息
        for item in items:
            # print item
            # 是否含有图片
            # haveImg = re.search("img", item[3])
            # # 如果不含有图片，把它加入 list 中
            # if not haveImg:
            replaceBR = re.compile('<br/>')
            text = re.sub(replaceBR, "\n", item[2])
            if isinstance(text,str):
                # item[0] 是一个段子的发布者，item[2] 是内容，item[1] 是等级, item[] 是点赞数,页码
                pageStories.append((item[0].strip(),item[1].strip(),text.strip(),item[3].strip(),pageIndex))
        return pageStories

    # 加载并提取页面的内容，加入到列表中
    def loadPage(self,pageIndex):
        pageStories = self.getPageItems(pageIndex)
        self.stories.append(pageStories)

    # 调用该方法，每次敲回车打印输出一个段子
    '''
    :return 作者、等级、内容、点赞数
    '''
    def getOneStory(self, pageStories)->tuple:
        # 遍历一页的段子
        for story in pageStories:
          return (story[0],story[1],story[2],story[3])

    # 开始方法
    def start(self):
        print ("开始读取数据")
        # 先加载一页内容
        while self.pageIndex <= self.maxPage:
            self.loadPage(self.pageIndex)
            self.pageIndex += 1
        print("数据采集结束")
        #开始写入数据库
        sql = """INSERT INTO story(author,levels,
                    content,likes,pageNo)
                values (%s,%s,%s,%s,%s)"""

        for pageStories in self.stories:
            mysql = DBHelper(sql,pageStories)
            mysql.executeMany()
            print("完成！")

spider = QSBK()
spider.start()
