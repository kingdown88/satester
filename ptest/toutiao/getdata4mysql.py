# coding=utf-8
'''
Project:读取mysql数据库的数据，转为json格式
'''
import test_json

import MySQLdb


def TableToJson():
    try:
        # 1-7：如何使用python DB API访问数据库流程的
        # 1.创建mysql数据库连接对象connection
        # connection对象支持的方法有cursor(),commit(),rollback(),close()
        conn = MySQLdb.Connect(host="127.0.0.1", user="root", passwd="root", db='zgd', port=3306,
                               charset='utf8')
        # 2.创建mysql数据库游标对象 cursor
        # cursor对象支持的方法有execute(sql语句),fetchone(),fetchmany(size),fetchall(),rowcount,close()
        cur = conn.cursor()
        # 3.编写sql
        sql = "SELECT item_id,title,chinese_tag FROM tt_data limit 100 ;"
        # 4.执行sql命令
        # execute可执行数据库查询select和命令insert，delete，update三种命令(这三种命令需要commit()或rollback())
        cur.execute(sql)
        # 5.获取数据
        # fetchall遍历execute执行的结果集。取execute执行后放在缓冲区的数据，遍历结果，返回数据。
        # 返回的数据类型是元组类型，每个条数据元素为元组类型:(('第一条数据的字段1的值','第一条数据的字段2的值',...,'第一条数据的字段N的值'),(第二条数据),...,(第N条数据))
        data = cur.fetchall()
        print u'fetchall()返回的数据：', data
        # 6.关闭cursor
        cur.close()
        # 7.关闭connection
        conn.close()
        jsonData = []
        # 循环读取元组数据
        # 将元组数据转换为列表类型，每个条数据元素为字典类型:[{'字段1':'字段1的值','字段2':'字段2的值',...,'字段N:字段N的值'},{第二条数据},...,{第N条数据}]
        for row in data:
            result = {}
            result['item_id'] = row[0]
            result['title'] = row[1]
            result['chinese_tag'] = row[2]
            jsonData.append(result)

    except:
        print 'MySQL connect fail...'
    else:
        # 使用json.dumps将数据转换为json格式，json.dumps方法默认会输出成这种格式"\u5377\u76ae\u6298\u6263"，加ensure_ascii=False，则能够防止中文乱码。
        # JSON采用完全独立于语言的文本格式，事实上大部分现代计算机语言都以某种形式支持它们。这使得一种数据格式在同样基于这些结构的编程语言之间交换成为可能。
        # json.dumps()是将原始数据转为json（其中单引号会变为双引号），而json.loads()是将json转为原始数据。
        print jsonData
        jsondatar = test_json.dumps(jsonData, ensure_ascii=False)
        print jsondatar
        jsondatar = test_json.dumps(jsonData)
        # 去除首尾的中括号
        return jsondatar[1:len(jsondatar) - 1]


if __name__ == '__main__':
    # 调用函数
    jsonData = TableToJson()
    print u'转换为json格式的数据：', jsonData
    # 以读写方式w+打开文件，路径前加r，防止字符转义
    f = open(r'c:\demo\getdata.txt', 'w+')
    # 写数据
    f.write(jsonData)
    # 关闭文件
    f.close()
