#urllib.error — Exception classes raised by urllib.request

The [urllib.error](https://docs.python.org/3/library/urllib.error.html#module-urllib.error) module defines the exception classes for exceptions raised by [urllib.request](https://docs.python.org/3/library/urllib.request.html#module-urllib.request). The base exception class is [URLError](https://docs.python.org/3/library/urllib.error.html#urllib.error.URLError).  
_urllib.error_模块定义了由[urllib.request](https://github.com/time-river/spider/blob/master/document/urllib_request.md)引起的一个异常类. 基本异常类是[urllib.error.URLError](#URLError).  

The following exceptions are raised by [urllib.error](https://docs.python.org/3/library/urllib.error.html#module-urllib.error) as appropriate:  
下列异常由_urllib.error_提出:(as appropriate: 酌情, 可不译)  

####_exception urllib.error.URLError_  
The handlers raise this exception (or derived exceptions) when they run into a problem. It is a subclass of [OSError](https://docs.python.org/3/library/exceptions.html#OSError).  
当handlers遇到问题, 会引发这些异常(或者派生的异常). 他是_OSError_的子类.  

#####_reason_  
The reason for this error. It can be a message string or another exception instance.  

_Changed in version 3.3:_ [URLError](https://docs.python.org/3/library/urllib.error.html#urllib.error.URLError) has been made a subclass of [OSError](https://docs.python.org/3/library/exceptions.html#OSError) instead of [IOError](https://docs.python.org/3/library/exceptions.html#IOError).  

####_exception urllib.error.HTTPError_  
Though being an exception (a subclass of [URLError](https://docs.python.org/3/library/urllib.error.html#urllib.error.URLError), an HTTPError can also function as a non-exceptional file-like return value (the same thing that [urlopen()](https://docs.python.org/3/library/urllib.request.html#urllib.request.urlopen) returns). This is useful when handling exotic HTTP errors, such as requests for authentication.  
尽管作为异常(_urllib.error.URLError_的子类), _urllib.error.HTTPError_也能执行这样的功能: 作为一个非特殊类文件返回值(类似于_urllib.request.urlopen()_返回的东西). 当操作 exotic HTTP errors时候非常有用, 例如 认证请求.  

#####_code_  
An HTTP status code as defined in [RFC 2616](http://www.faqs.org/rfcs/rfc2616.html). This numeric value corresponds to a value found in the dictionary of codes as found in [http.server.BaseHTTPRequestHandler.responses](https://docs.python.org/3/library/http.server.html#http.server.BaseHTTPRequestHandler.responses).  

#####_reason_  
This is usually a string explaining the reason for this error.  

#####_headers_
The HTTP response headers for the HTTP request that caused the [HTTPError](https://docs.python.org/3/library/urllib.error.html#urllib.error.HTTPError).

_New in version 3.4._

####_exception urllib.error.ContentTooShortError(msg, content)_  
This exception is raised when the [urlretrieve()](https://docs.python.org/3/library/urllib.request.html#urllib.request.urlretrieve) function detects that the amount of the downloaded data is less than the expected amount (given by the _Content-Length_ header). The content attribute stores the downloaded (and supposedly truncated) data.

====
```
2015 11.2 晚
```
