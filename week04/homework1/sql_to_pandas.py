"""
coding:utf8
@Time : 2020/8/12 22:58
@Author : cjr
@File : sql_to_pandas.py
"""

import pandas as pd
import pymysql

sql = 'select * from movies'

conn = pymysql.connect(
    host='47.105.70.179',
    user='root',
    password='wawy5211314',
    database='maoyan',
    port=3306,
    charset='utf8')

pf = pd.read_sql(sql, conn)
# 1. SELECT * FROM data;
print(f'全部数据\n'
      f'{pf}')
# 2. SELECT * FROM data LIMIT 10;
print(f'前十数据\n'
      f'{pf.head(10)}')
# 3. SELECT id FROM data;  //id 是 data 表的特定一列
print(f'特定列ID\n'
      f'{pf["id"]}')
# 4. SELECT COUNT(id) FROM data;
print(f'特定列ID的个数\n'
      f'{pf["id"].size}')
# 5. SELECT * FROM data WHERE id<5 AND movie_time="测试";
print(f'where查询\n'
      f'{pf[(pf.id<5)&(pf.movie_name=="测试")]}')
# 6. SELECT id,COUNT(DISTINCT movie_name) FROM table1 GROUP BY id;
print(f'分组查询\n'
      f'{pf.groupby("id").agg({"movie_name": pd.Series.nunique})}')
# 7. SELECT * FROM table1 t1 INNER JOIN table2 t2 ON t1.id = t2.id; 我的库里没有两张表这个验证不了
print(f'内连接查询\n'
      f'{pf.merge("table1", "table2", how="inner", left_on="id", right_on="id")}')
# 8. SELECT * FROM table1 UNION SELECT * FROM table2;  虚构一个表2，未能验证正确性
pf2 = sql = 'select * from music'
print(f'多表联合查询\n'
      f'{pf.append(pf2)}')
# 9. DELETE FROM table1 WHERE id=10;
print(f'删除表中指定元素\n'
      f'{pf.drop(pf[pf.id == "10"].index)}')
# 10. ALTER TABLE table1 DROP COLUMN column_name;
print(f'删除表中指定列\n'
      f'{pf.drop(["movie_type"], axis=1)}')

