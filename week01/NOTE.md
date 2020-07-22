学习笔记

函数：pandas.DataFrame.to_csv

参数：

sep，入参文件为可迭代对象时候使用该参数设定分隔符号，默认是逗号

index，Boole类型，在文件迭代时候是否添加序号，默认添加（True）

quotechar，官方文档解释是用来引用字段的字符，即当出现换行时候该换行符的前后被认为是两个字段，所以会用这个参数的值引起来，默认是双引号

line_terminator，换行符的表示形式，默认是用os.linesep函数进行获取的

