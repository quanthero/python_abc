#-*- coding: utf-8 -*-
"""
Created on Sat Feb 10 18:44:25 2018

@author: Sheng
"""
#导入两个模块
import baostock as bs
import pandas as pd

# 首先通过ts.get_stock_basics()命令获得股票代码的一些基本数据 ，然后通过to_excel()命令保存。
    # 以下是本人保存的路径
source_date=r'E:\\Quant\\Baostock\\Data\\index\\sz50_stocks.csv'

# 我们需要提取股票代码，用于后面的for循环，首先读取之前下载好的文件，将第一列的股票代码进行字符串转化。
df=pd.read_csv(source_date,converters={'code':lambda x:str(x)})

# 将提取出来的股票代码列表化赋值与 stockcode 这个变量。
stockcode=list(map(str,df['code']))

# 开始进行循环下载。。
for i in stockcode:
    print('开始下载{}股票数据.....'.format(i))

    #设定每个文件的文件名和存储地址。
    file_address=r'E:\\Quant\\Baostock\\Data\\stock\\{}.csv'.format(i)

    #提取单个股票的历史数据。
    lg = bs.login()
    # 显示登陆返回信息
    print('login respond error_code:'+lg.error_code)
    print('login respond  error_msg:'+lg.error_msg)
    rs=bs.query_history_k_data_plus(i,
    "date,time,code,open,high,low,close,volume,amount,adjustflag",
    start_date='2010-01-01', end_date='2019-12-31',
    frequency="5", adjustflag="3")
    print('query_history_k_data_plus respond error_code:'+rs.error_code)
    print('query_history_k_data_plus respond error_msg:'+rs.error_msg)
    #导出到之前设定的好的文件地址。
    data_list = []
    while (rs.error_code == '0') & rs.next():
    # 获取一条记录，将记录合并在一起
        data_list.append(rs.get_row_data())
    result = pd.DataFrame(data_list, columns=rs.fields)
    result.to_csv(file_address)
    #print(result)

    #由于导出的每个股票的历史数据中并没有包含股票代码，所以我把股票代码加入到Excel中，
    #在日期的后一列加入股票代码，方便以后所有数据整合后可以进行股票筛选。
    #如果不需要，可以删除下面三行代码。
    # dw_data=pd.read_csv(file_address)
    # dw_data.insert(loc=1,column='code',value=i)
    # dw_data.to_csv(file_address)

    # 打印出下载进程，方便观察。。。
    print('{}/{} has been downloaded,{}股票数据下载完毕'
           .format(stockcode.index(i)+1,len(stockcode),i))
    print('-----------------------------------------------------')