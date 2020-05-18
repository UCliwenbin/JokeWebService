'''
Created on 2020-05-16 22:22
@description  数据库操作工具
@author mac
@name mySqlUtil
'''

import pymysql
import logging
from mysql.config import db_config

class DBHelper():
    # 构造函数,初始化数据库连接
    def __init__(self,sql,params=None):
        self.sql = sql
        self.params = params
        self.conn = None
        self.cur = None

    def connectiondatabase(self):
        print(db_config['host'],db_config['username'],db_config['password'],db_config['database'],db_config['charset'])
        try:
            self.conn = pymysql.connect(db_config['host'],db_config['username'],
                                    db_config['password'],db_config['database'],charset=db_config['charset'])
        except:
            logging.error("connectDatabase failed")
            return False
        self.cur = self.conn.cursor()
        return True



    # 关闭数据库
    def closedatabase(self):
        # 如果数据打开，则关闭；否则没有操作
        if self.conn and self.cur:
            self.cur.close()
            self.conn.close()
        return True

    # 执行数据库的sq语句,主要用来做插入操作
    def execute(self):
        self.connectiondatabase()
        try:
            if self.conn and self.cur:
                # 正常逻辑，执行sql，提交操作
                self.cur.execute(self.sql,self.params)
                self.conn.commit()
        except:
            self.conn.rollback()
            logging.error("execute failed: " + self.sql)
            logging.error("params: " + self.params)
            self.closedatabase()
            return False
        return True
    #批量插入
    def executeMany(self):
        self.connectiondatabase()
        try:
            if self.conn and self.cur:
                # 正常逻辑，执行sql，提交操作
                self.cur.executemany(self.sql,self.params)
                self.conn.commit()
        except:
            # self.conn.rollback()
            logging.error("execute failed: " + self.sql)
            logging.error("params: " + self.params)
            # self.closedatabase()
            # return False
        return True

    # 用来查询表数据
    def select(self):
        self.connectiondatabase()
        self.cur.execute(self.sql,self.params)
        result = self.cur.fetchall()
        return result

'''
查询操作，插入操作
   param = "Test page title"
    sql = "select * from pages where title=%s"
    mysql = DBHelper(sql,param)
    rest = mysql.select()
    row = rest[0]
    title = row[1]
    content = row[2]
    time = row[3]
    print('title=%s,content=%s,time=%s'% (title,content,time))
'''
if __name__ == '__main__':
    sql = """INSERT INTO story(author,
                    likes,content,levels,pageNo)
                    values (%s,%s,%s,%s,%s)"""

    mysql = DBHelper(sql,('净心居士', '19', '中午下班和同事一起去食堂，突然要方便下。于是我说道:我要去方便下，你们等我会回来一起吃💩\n周围的同事都用看沙 雕 的眼神看着我[捂脸]','896', 6))
    mysql.execute()