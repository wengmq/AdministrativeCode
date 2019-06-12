# -*- coding: UTF-8 -*-
import pymysql
import requests
from bs4 import BeautifulSoup
import json
import data


# 打开数据库连接
#地址：本机ip
#账号：root
#密码：990124
#数据库名：mysqldb
#字符编码：utf8
db = pymysql.connect("localhost", "root", "990124", "mysqldb", charset='utf8' )
# 使用cursor()方法获取操作游标
cursor = db.cursor()

#函数功能创建一个表
def createTable():
    # 如果数据表已经存在使用 execute() 方法删除表。
    cursor.execute("DROP TABLE IF EXISTS CHART")
    sql = """CREATE TABLE CHART (
             CHART_NAME  CHAR(50),
             CHART_CODE  CHAR(50)
              )"""

    #执行SQL语句
    cursor.execute(sql)
#createTable()


#函数功能：往数据库中插入数据
def write2MYSQL(CHART_NAME,CHART_CODE):
    sql = 'INSERT INTO CHART(CHART_NAME,CHART_CODE)VALUES("%s","%s")' % \
          (CHART_NAME, CHART_CODE)
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        # Rollback in case there is any error
        db.rollback()




#函数功能： 用来把数据读取到MYSQL数据库中
def readData():
    d = json.dumps(data.d1)
    print(type(d))
    print(type(data.d1))

    print(d)

    list1 = data.d1
    for dict1 in list1:
        #省份
        print(dict1.get('name'),end='')
        print(dict1.get('code'))
        write2MYSQL(dict1.get('name'), dict1.get('code'))
        #市
        if 'children' in dict1.keys():
            list2 = dict1.get('children')
            for dict2 in list2:
                print(dict2.get('name'), end='')
                print(dict2.get('code'))
                write2MYSQL(dict2.get('name'), dict2.get('code'))
                #区
                if 'children' in dict2.keys():
                    list3 = dict2.get('children')
                    for dict3 in list3:
                        print(dict3.get('name'), end='')
                        print(dict3.get('code'))
                        write2MYSQL(dict3.get('name'), dict3.get('code'))
#readData();

while 1:
    name = input("请输入您要查询的地区名：")

    sql = 'SELECT CHART_CODE FROM mysqldb.chart where CHART_NAME = "%s"' % (name)
    #print(sql);

    # 使用execute方法执行SQL语句
    cursor.execute(sql)

    # 使用 fetchone() 方法获取一条数据
    data = cursor.fetchone()
    if (data == None):
        print('该地区不存在！请重新输入！')
    else:
        print ( name+"的邮政编码是 : %s " % data)

