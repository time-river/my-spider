#json -- JSON encoder and decoder

JSON (JavaScript Object Notation), 在[RFC 7159](http://tools.ietf.org/html/rfc7159.html)(废除了[RFC 4627](http://tools.ietf.org/html/rfc4627.html))与[ECMA-404](http://tools.ietf.org/html/rfc4627.html)中详细说明， 它是受JavaScript对象文字语法启发的一个轻量级的数据交换格式（尽管它不完全是JavaScript的子集）。
[json](https://docs.python.org/3/library/json.html#module-json)提供了对用户友好的[marshal](https://docs.python.org/3/library/marshal.html#module-marshal)与[pickle]( pickle)的API标准库。

基本的Python对象层次编码：
```
>>> import json
>>> json.dumps(['foo', {'bar': ('baz', None, 1.0, 2)}])
'["foo", {"bar": ["baz", null, 1.0, 2]}]'
>>> print(json.dumps("\"foo\bar"))
"\"foo\bar"
>>> print(json.dumps('\u1234'))
"\u1234"
>>> print(json.dumps('\\'))
"\\"
>>> print(json.dumps({"c": 0, "b": 0, "a": 0}, sort_keys=True))
{"a": 0, "b": 0, "c": 0}
>>> from io import StringIO
>>> io = StringIO()
>>> json.dump(['streaming API'], io)
>>> io.getvalue()
'["streaming API"]'
```
紧凑的编码：
```
>>> import json
>>> json.dumps([1,2,3,{'4': 5, '6': 7}], separators=(',', ':'))
'[1,2,3,{"4":5,"6":7}]'
```
漂亮的输出：
```
>>> import json
>>> print(json.dumps({'4': 5, '6': 7}, sort_keys=True, indent=4))
{
    "4": 5,
    "6": 7
}
```
JSON解码：
```
>>> import json
>>> json.loads('["foo", {"bar":["baz", null, 1.0, 2]}]')
['foo', {'bar': ['baz', None, 1.0, 2]}]
>>> json.loads('"\\"foo\\bar"')
'"foo\x08ar'
>>> from io import StringIO
>>> io = StringIO('["streaming API"]')
>>> json.load(io)
['streaming API']
```
指定JSON对象的编码：
```
>>> import json
>>> def as_complex(dct):
...     if '__complex__' in dict:
...         return complex(dct['real'], dct['imag'])
...     return dic
...
>>> json.loads('{"__complex__": true, "real": 1, "imag": 2}'),
...     object_hook=as_complex
(1+2j)
>>> import decimal
>>> json.loads('1.1', parse_float=decimal.Decimal)
Decimal('1.1')
```
拓展的[JSONEncoder](https://docs.python.org/3/library/json.html#json.JSONEncoder)：
```
>>> import json
>>> class ComplexEncoder(json.JSONEncoder):
...     def default(self, obj):
...         if isinstance(obj, complex):
...             return [obj.real, obj.imag]
...         # Let the base class default method raise the TypeError
...         return json.JSONEncoder.default(self, obj)
...
>>> json.dumps(2 + 1j, cls=ComplexEncoder)
'[2.0, 1.0]'
>>> ComplexEncoder().encode(2 + 1j)
'[2.0, 1.0]'
>>> list(ComplexEncoder().iterencode(2 + 1j))
['[2,0', ', 1.0', ']']
```
在shell中使用json.tool来证实与打印：
```
$ echo '{"json":"obj"}' | python -m json.tool
{
    "json": "obj"
}
$ echo '{1.2:3.4}' | python -m json.tool
Expecting property name enclosed in double quotes: line 1 column 2 (char 1)
```

####基本用法

#####_json.dump(obj, fp, skipkeys=False, ensure_ascii=True, check_circular=True, allow_nan=True, cls=None, indent=None, separators=None, default=None, sort_keys=False, **kw)_

根据[_conversion table_](https://docs.python.org/3/library/json.html#py-to-json-table)将_obj_格式化为JSON，然后输入至_fp_（a `.write()`-支持[_file-like object](https://docs.python.org/3/glossary.html#term-file-like-object)
如果_skipkeys_为`True`（默认`False`）,那么不是基本类型(`str`, `int`, `float`, `bool`, `None`)的dict keys将被忽略，会引发一个_TypeError_。
_JSON_模块总产生_str_对象，不是_bytes_对象。因此，`fp.write()`必须支持_str_的写入。
如果_ensure_ascii_为`True`（默认值），那么必须保证输出是所有传入的non-ASCII字符转义。如果_ensure_ascii为`False`，那么字符将按原样输出。
如果_check_circular_为`False`（默认`True`），那么对容器类型的循环引用检查将被忽略，一个循环引用将导致_OverflowError_（或者更糟糕）。  
如果_allow_nan_为`False`（默认`True`），那么在严格JSON规范下，序列化的浮点值范围将引发一个_ValueError_。  
如果_indent_是一个非负的整数或字符串，那么JSON数组与对象成员将按照原有的缩进程度打印。缩进程度为0,或者复数，或`""`的将被插入至新的一行。`None`（默认值）选择最紧凑的表示方式。使用正整数，那么会在每行缩进指定的空格数。  
_separators_应该是一个`(item_separator, key_separator)`元组。3.4版本后默认值为`(', ', ':')`。  
_default(obj)_是一个返回序列化版本的_obj_的函数，或者引发一个_TypeError_。默认只引发_TypeError_。  
如果_sort_keys_为`True`（默认`False`），那么输出的字典将按照key排序。  

#####_json.dumps(obj, skipkeys=False, ensure_ascii=True, check_circular=True, allow_nan=True, cls=None, indent=None, separators=None, default=None, sort_keys=False, **kw)_

使用_conversion table_将_obj_格式化为str。参数含义与_dump()_相同。  

#####_json.load(fp, cls=None, object_hook=None, parse_float=None, parse_int=None, parse_constant=None, object_pairs_hook=None, **kw)_

使用_conversion table_将_fp_（包含JSON文档的、支持_file-like object_的a`.read`）格式化为Python对象。  

#####_json.loads(s, encoding=None, cls=None, object_hook=None, parse_float=None, parse_int=None, parse_constant=None, object_pairs_hook=None, **kw)_

使用_conversion table_将s（一个具有JSON文档的_str_实例）转化为Python对象。
