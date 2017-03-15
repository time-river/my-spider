###关于Python3的一点前置知识

####数据类型

1. Booleans[布尔]型: True or False
* Numbers[数值型]: Integers, Floats, Fractions(import fractions); even Complex Number
* [String[字符串型]](#String): a sequence of Unicode characters
* [Bytes[字节] & Byte Arrays[字节数组](#Byte): for example, a JPEG image
* [Lists[列表]](#Lists): 是值的有序序列
* [Tuples[元组]](#Tuples): 是有序而不可变的值序列
* [Sets[集合]](#Sets): 是装满无序值的包裹(见集合的数学定义)
* [Dictionaries[字典]](#Dictionaries): 是键值对的包裹(包裹理解为集合)

在Python中一切均为对象,因此存在像_module[模块]_, _function[函数]_, _class[类]_, _method[方法]_, _file[文件]_, 甚至 _compile code[已编译代码]_ 这样的类型.  

====

#####<a id="Lists">Lists[列表]</a>

* 创建&读取
* 切片
* 新增项
```
>>>a_list = ['a']

>>>a_list = alist + [2.0, 3] // + 运算符连接列表可以创建一个新列表
>>>a_list                    // 列表可以包含任何数据类型
['a', 2.0, 3]

>>>a_list.append(True) // append()方法向列表尾部添加一个新元素
>>>a_list
['a', 2.0, 3, True]

>>>a_list.extend(['four', 'Ω']) // 因列表以类的方式实现, 创建列表实际上是将一个类实例化
>>>a_list                       // extend()方法将参数(仅列表)中每个元素都添加到原有的列表中
['a', 2.0, 3, True, 'four', 'Ω']

>>>a_list.insert(0, 'Ω']) // insert()方法将单个元素插入到列表中指定的索引位置
>>>a_list
['Ω', 'a', 2.0, 3, True, 'four', 'Ω']

注:
  append()方法只接受一个参数,但可以是任何数据类型
  extend()方法只接受一个参数,该参数总是一个列表
```

* 检索值
```
>>>a_list = ['a', 'b', 'new', 'mpilgrim', 'new']

>>>a_list.count('new') // count()方法返回列表中某个特定值出现的次数
2

>>>'new' in a_list // in 运算符返回Ture或False
True

>>>a_list.index('mpilgrim') // index()方法查找某值在列表中第一次出现的位置
3                           // 0为基点
>>>a_list.index('c') // 查找不到引发一个例外
Traceback (innermost last):
  File "<interactive input>", line 1, in ?ValueError: list.index(x): x not in list
```
* 删除元素
```
>>>a_list = ['a', 'b', 'new', 'mpilgrim', 'new']

>>>del a_list[1] // 使用del删除某个特定元素
>>>a_list
['a', 'new', 'mpilgrim', 'new']

>>>a_list.remove('new') // 通过remove()方法从列表中删除某个第一次出现的元素
>>>a_list
['a', 'mpilgrim', 'new']

>>>a_list.remove('b') // 试图删除列表中不存在的元素将引发一个例外
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ValueError: list.remove(x): x not in list

>>>a_list.pop(1) // pop()方法删除指定索引位置的元素, 并返回其值
'mpligrim'

>>>a_list.pop() // 无参数则删除并返回最后一个元素的值
'new'

>>>a_list.pop()
'a'

>>>a_list.pop() // 对空列表使用该方法将引发一个例外
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
IndexError: pop from empty list

关于布尔上下文环境中的列表:
  空列表为False
  任何至少包含一个以上元素的列表为True, 元素的值无关紧要. 如, [False]为真.
```
* `list()`函数接受一个元组参数并返回一个列表

#####<a id="Tubles">Tubles[元组]</a>

* 内建`tuple()`函数接收一个列表函数, 返回一个元组
* 元组定义方式与列表相同, 但用圆括号而不是方括号闭合
* 但元素元组需要在值后面加一个逗号. 如, `(False)`
* 元组有列表一样的切片方法, 计数方式
* 无法添加元素
* 可以查找元素与使用`in`运算符
* 不能删除元素
* 布尔上下文环境中与列表一样
* 利用元组同时赋予多个值
```
>>>v = ('a', 2, True)
>>>(x, y, z) = z
>>>x
'a'
>>>y
2
>>>z
True
```

#####<a id="Sets">Sets[集合]</a>

* 集合是无序的
* 集合创建
```
>>>a_set = {1} // 创建一个值的集合仅需将改值放在花括号中间
>>>type(a_set)
<class 'set'>
>>>b_set = {1, 2, 3} // 多值集合将值用逗号隔开

>>>a_list = ['a', 'b', 'mpilgrim', True, False, 42]
>>>a_set = set(a_list) // 以列表为基础创建集合
>>>a_set
{'a', 'b', 'mpilgrim', True, False, 42}

>>>a_set = set() // 创建空集合
>>>a_set
set()
>>>type(a_set)
<class 'set'>
>>>not_sure = {}
>>>type(not_sure)
<class 'dict'>
```
* 修改集合
  * add()方法接受单个可以是任何数据类型的参数, 并将该值添加到集合之中
  * update()方法接受一个集合作为参数, 并将其所有成员添加到初始表中, 行为方式是对参数集合中每个成员调用add()方法
  * update()方法还可以接受一些其它数据类型的对象作为参数, 包括列表
* 从集合中删除元素
  * discard()方法: 接受一个单值作为参数, 并从集合中删除该值, 若删除不存在的值, 只是一条不进行任何操作的空指令
  * remove()方法: 同discard(), 不同在于删除不存在的值时候, 会引发一个KeyError例外
  * pop()方法: 同列表
  * clear()方法: 删除集合中所有值, 等价于a_set = set()
* 常见集合操作
  * in
  * union()方法: `a_set.union(b_set)` 并运算
  * intersection()方法: `a_set.intersection(b_set)` 交运算
  * difference()方法: `a_set.a_difference(b_set)` a_set - b_set
  * symmetric_difference()方法: `a_set.symmetric_difference(b_set)` 交之补
  * issuperset()方法
* 布尔上下文环境中的集合
  * 空集合为假
  * 非空集合为真, 元素值无关紧要

#####<a id="Dictionaries>Dictionaries[字典]</a>

* 字典是键值对的集合
* 创建
```
>>>a_dict = {'server': 'db.diveintopyhon3.ort', 'database': 'mysql'}
>>>a_dict['server']
'db.diveintopyhon3.ort'

>>>a_list_of_lists = [['user', 'pilgrim'], ['database', 'master'], ['password', 'PapayaWhip']]
>>>a_dict = dict(a_list_of_lists)
>>>a_dict
{'password': 'PapayaWhip', 'user': 'pilgrim', 'database': 'master'}
```
* 修改
* 混合值字典
* 布尔上下文中的字典

#####<a id="String">String[字符串]</a>

* Unicode
  * UTF-32
  * UTF-16
  * UTF-8
* 字节非字符
* Python3中, 所有字符串皆是Unicode编码
* 创建
* 格式化字符串
```
>>>username = 'mark'
>>>password = 'PapayaWhip'
>>>"{0}'s password is {1}".format(username, password) // {0} {1}为替换字段
"mark's password is PapayaWhip"                       // 被format()方法替换
```
  * 复合字段名: 格式说明符可以通过利用(类似)Python的语法访问到对象的元素或属性
    * 使用列表作为参数, 并且通过下标索引来访问其元素
    * 使用字典作为参数, 并且通过键来访问其值
    * 使用模块作为参数, 并且通过名字来访问其变量及函数
    * 使用类的实例作为参数, 并且通过名字来访问其方法和属性
    * 以上方法的任意组合皆为有效复合字段名
```
>>>SUFFIXES = {1000: ['KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'],
            1024: ['KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB']}
>>>si_suffixes = SUFFIXES[1000]
>>>'1000{0[0]} = 1{0[1]}'.format(si_suffixes)    
'1MB = 1000KB'
>>>'1MB = 1000{0.modules[
```
* 其他常用方法
  * splitlines()
  * lower()
  * count()
* 字符串分片

#####<a id="Byte">[Bytes[字节] & Byte Arrays[字节数组]</a>

* 字节即字节; 字符是一种抽象. 一个不可变的Unicode编码的字符序列叫做String, 一串由0到255之间的数字组成的序列叫做bytes对象.
```
>>>by = b'abcd\x65' \\ bytes对象定义
>>>by
b'abcde'
>>>type(by)
<class 'bytes'>
>>>len(by)
5
>>>by += b'\xff'
>>>by
b'abcdf\xff'
>>>len(by)
6
>>by[0]
97
>>>by[0] = 102 \\ bytes不可变
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'bytes' object does not support item assignment
>>>barr = bytearray(by) \\ 使用bytearray()函数完成从bytes对象到bytearray对象转变
>>>barr
bytearray(b'abcde\xff')
>>>len(barr)
6
>>>barr[0] = 102 \\ bytes对象与bytearray对象不同点
>>>barr
bytearray(b'fbcde\xff')

>>>by = b'd'
>>>s = 'abcde'
>>>by + s
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: can't concat bytes to str
>>>s.count(by)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: Can't convert 'bytes' object to str implicitly
>>>s.count(by.decode('ascii')) // bytes对象decode()方法按照某种编码方式将bytes对象转换为字符串
1
```
* decode()方法 & encode()方法
* `# -*- coding: utf-8 -*-`
* 计算机内存中, 统一使用Unicode编码, 当需要保存到硬盘或者需要传输的时候, 就转换为UTF-8编码
* 浏览网页的时候, 服务器会把动态生成的Unicode内容转换为UTF-8再传输到浏览器
urllib.request.openurl()
