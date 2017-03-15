####_urllib.parse.urlencode(query, doseq=False, safe='', encoding=None, errors=None, quote_via=quote_plus)_

Convert a mapping object or a sequence of two-element tuples, which may contain [str](https://docs.python.org/3/library/stdtypes.html#str) or [bytes](https://docs.python.org/3/library/functions.html#bytes) objects, to a “percent-encoded” string. If the resultant string is to be used as a _data_ for POST operation with [urlopen()](https://docs.python.org/3/library/urllib.request.html#urllib.request.urlopen) function, then it should be properly encoded to bytes, otherwise it would result in a [TypeError](https://docs.python.org/3/library/exceptions.html#TypeError).  
把包含有[str!!]()或者[bytes!]()对象的

The resulting string is a series of `key=value` pairs separated by `'&'` characters, where both _key_ and _value_ are quoted using the _quote_via_ function. By default, [quote_plus()](https://docs.python.org/3/library/urllib.parse.html#urllib.parse.quote_plus) is used to quote the values, which means spaces are quoted as a `'+'` character and ‘/’ characters are encoded as `%2F`, which follows the standard for GET requests (`application/x-www-form-urlencoded`). An alternate function that can be passed as _quote_via_ is [quote()](https://docs.python.org/3/library/urllib.parse.html#urllib.parse.quote), which will encode spaces as `%20` and not encode ‘/’ characters. For maximum control of what is quoted, use `quote` and specify a value for _safe_.

When a sequence of two-element tuples is used as the _query_ argument, the first element of each tuple is a key and the second is a value. The value element in itself can be a sequence and in that case, if the optional parameter doseq is evaluates to _True_, individual `key=value` pairs separated by `'&'` are generated for each element of the value sequence for the key. The order of parameters in the encoded string will match the order of parameter tuples in the sequence.

The _safe_, _encoding_, and _errors_ parameters are passed down to _quote_via_ (the _encoding_ and _errors_ parameters are only passed when a query element is a [str](https://docs.python.org/3/library/stdtypes.html#str)).

To reverse this encoding process, [parse_qs()](https://docs.python.org/3/library/urllib.parse.html#urllib.parse.parse_qs) and [parse_qsl()](https://docs.python.org/3/library/urllib.parse.html#urllib.parse.parse_qsl) are provided in this module to parse query strings into Python data structures.

Refer to [_urllib examples_](https://docs.python.org/3/library/urllib.request.html#urllib-examples) to find out how urlencode method can be used for generating query string for a URL or data for POST.

_Changed in version 3.2:_ Query parameter supports bytes and string objects.

_New in version 3.5:_ _quote_via_ parameter.
