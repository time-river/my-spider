#####_urllib.request.urlopen(url, data=None, [timeout, ]*, cafile=None, capath=None, cadefault=False,context=None)_

Open the URL _url_, which can be either a string or a [Request](https://docs.python.org/3/library/urllib.request.html#urllib.request.Request) object.  
打开一个名为_url_的URL(Uniform Resource Locator:统一资源定位符),url可以是一个字符串或者一个[urllib.request.Request](#Request)对象.   

_data_ must be a bytes object specifying additional data to be sent to the server, or `None` if no such data is needed. _data_ may also be an iterable object and in that case Content-Length value must be specified in the headers. Currently HTTP requests are the only ones that use data; the HTTP request will be a POST instead of a GET when the data parameter is provided.  
_data_必须是指定要发送给服务器的额外bytes object(一串由0到255之间的数字组成的序列叫做bytes对象),或者`None`(若不需要这样的数据的话)._data_还可以是可迭代对象,这种情况下,必须在headers中明确指出Content-Length(在entity-header field中，它指出entity-body大小，[w3](http://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html)参考)的值.目前,仅有HTTP请求使用_data_;如果_data_参数被提供,HTTP请求将会使用POST方法而不是GET方法.  

_data_ should be a buffer in the standard _application/x-www-form-urlencoded_ format. The [urllib.parse.urlencode()](https://docs.python.org/3/library/urllib.parse.html#urllib.parse.urlencode) function takes a mapping or sequence of 2-tuples and returns a string in this format. It should be encoded to bytes before being used as the data parameter. The charset parameter in `Content-Type` header may be used to specify the encoding. If charset parameter is not sent with the Content-Type header, the server following the HTTP 1.1 recommendation may assume that the data is encoded in ISO-8859-1 encoding. It is advisable to use charset parameter with encoding used in `Content-Type` header with the [Request](https://docs.python.org/3/library/urllib.request.html#urllib.request.Request).  
_data_应该是采用标准_application/x-www-form-urlencoded_形式的buffer。 [urllib.parse.urlencode()!!]()函数可接受映射对象或者2-元组序列,且会返回这种格式的字符串.它应该在作为_data_参数使用前被编码为bytes.在`Content-Type`头(内容类型实体头域指出媒体类型，[w3](http://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html)参考)中的charset parameter可用于指定编码方式.若charset parameter(字符集参数)不以Content-Type header方式发送,且假定服务器遵循推荐的HTTP1.1,那么数据会采用ISO-8859-1编码方式进行编码.明智的做法是使用具有[urllib.request.Request!!)[]的`Content-Type` header编码的charset parameter.  

_urllib.request_ module uses HTTP/1.1 and includes `Connection:close` header in its HTTP requests.  
_urllib.request_模块使用HTTP/1.1，且其HTTP请求包括`Connection:close`头.  

The optional _timeout_ parameter specifies a timeout in seconds for blocking operations like the connection attempt (if not specified, the global default timeout setting will be used). This actually only works for HTTP, HTTPS and FTP connections.  
可选的_timeout_参数在进行类似尝试连接的阻塞操作(block operations)时候,指定以秒为单位(若不指定,则会使用全局默认超时设置).实际上,这仅适用于HTTP,HTTPS及FTP连接.   

If context is specified, it must be a [ssl.SSLContext](https://docs.python.org/3/library/ssl.html#ssl.SSLContext)  instance describing the various SSL options. See [HTTPSConnection](https://docs.python.org/3/library/http.client.html#http.client.HTTPSConnection) for more  details.  
如果_context_被指定,它必须是一个描述不同SSL选项的[ssl.SSLContext](https://docs.python.org/3/library/ssl.html#ssl.SSLContext)实例.请看[HTTPSConnection](https://docs.python.org/3/library/http.client.html#http.client.HTTPSConnection)获取更多信息.  

The optional _cafile_ and _capath_ parameters specify a set of trusted CA certificates for HTTPS requests. _cafile_ should point to a single file containing a bundle of CA certificates, whereas _capath_ should point to a directory of hashed certificate files. More information can be found in [ssl.SSLContext.load_verify_locations()](https://docs.python.org/3/library/ssl.html#ssl.SSLContext.load_verify_locations).  
可选的_cafile_和_capath_参数指定了HTTPS请求中可信赖的CA证书集._cafile_应指向包含一系列CA证书的单个文件,而_capath_应指向hashed certificated files的工作目录.在[ssl.SSLContext.load_verify_locations()](https://docs.python.org/3/library/ssl.html#ssl.SSLContext.load_verify_locations)中可找到更多相关信息.  

The _cadefault_ parameter is ignored.  
忽略_cadefault_参数.  

For http and https urls, this function returns a [http.client.HTTPResponse](https://docs.python.org/3/library/http.client.html#http.client.HTTPResponse) object which has the following [_HTTPResponse Objects_](https://docs.python.org/3/library/http.client.html#httpresponse-objects) methods.   
对于http与https url而言,该函数会返回一个遵守[_HTTPResponse Objects_](https://github.com/time-river/spider/blob/master/document/HTTPResponseObjects.md)方法的_http.client.HTTPResponse_对象.  

For ftp, file, and data urls and requests explicitly handled by legacy [URLopener](https://docs.python.org/3/library/urllib.request.html#urllib.request.URLopener) and [FancyURLopener](https://docs.python.org/3/library/urllib.request.html#urllib.request.FancyURLopener) classes, this function returns a _urllib.response.addinfourl_ object which can work as [_context manager_](https://docs.python.org/3/glossary.html#term-context-manager) and has methods such as
　geturl() — return the URL of the resource retrieved, commonly used to determine if a redirect was followed  
　info() — return the meta-information of the page, such as headers, in the form of an [email.message_from_string()](https://docs.python.org/3/library/email.parser.html#email.message_from_string) instance (see [Quick Reference to HTTP Headers](http://www.cs.tut.fi/~jkorpela/http.html)  
　getcode() – return the HTTP status code of the response.  
对于ftp,文件,数据URL以及可通过传统[urllib.request.URLopener!!]()和[urllib.request.FancyURLopener!!]()类处理的明确请求而言，该函数会返回可作为[context manager](https://docs.python.org/3/glossary.html#term-context-manager)工作且具有这些方法的[_urllib.response.addinfourl_!!]()对象:  
　_geturl()_--返回源检索URL,常用于确定是否遵从重定向  
　_info()_--以[email.message_from_string()](https://docs.python.org/3/library/email.parser.html#email.message_from_string)实例形式返回页面meta-infomation，例如headers(请参阅[Quick Reference to HTTP Headers](http://www.cs.tut.fi/~jkorpela/http.html))  
　_getcode()_--返回HTTP响应状态码  

Raises [URLError](https://docs.python.org/3/library/urllib.error.html#urllib.error.URLError) on errors.  
出错时候会引发[urllib.error.URLError!!]()错误.  

Note that `None` may be returned if no handler handles the request (though the default installed global [OpenerDirector](https://docs.python.org/3/library/urllib.request.html#urllib.request.OpenerDirector) uses [UnknownHandler](https://docs.python.org/3/library/urllib.request.html#urllib.request.UnknownHandler) to ensure this never happens).  
注意:如果没有程序处理请求的话(尽管默认安装了全局的[urllib.request.OpenerDirector!!]()使用[urllib.request.UnknownHandler!!]()来确保这永远不会发生),会返回`None`.  

In addition, if proxy settings are detected (for example, when a _*\_proxy_ environment variable like http\_proxy is set), [ProxyHandler](https://docs.python.org/3/library/urllib.request.html#urllib.request.ProxyHandler) is default installed and makes sure the requests are handled through the proxy.  
此外,若检测到代理设置(比如，当设置了类似于http\_proxy的_*\_proxy_环境变量时),由于[urllib.request.ProxyHandle!!]()已默认安装,会确保请求是通过代理进行处理.   

The legacy `urllib.urlopen` function from Python 2.6 and earlier has been discontinued; [urllib.request.urlopen()](https://docs.python.org/3/library/urllib.request.html#urllib.request.urlopen) corresponds to the old `urllib2.urlopen`. Proxy handling, which was done by passing a dictionary parameter to `urllib.urlopen`, can be obtained by using [ProxyHandler objects](https://docs.python.org/3/library/urllib.request.html#urllib.request.ProxyHandler).  
Python2.6以及之前的版本已经停用了传统的`urllib.urlopen`函数;[urllib.request.urlopen()!!]()对应旧的`urllib2.urlopen`.通过把字典参数传递给`urllib.urlopen`可进行代理操作,通过使用[urllib.request.ProxyHandler!!]()对象也可以获得代理处理.  

_Changed in version 3.2:_ _cafile_ and _capath_ were added.  
_Changed in version 3.2:_ HTTPS virtual hosts are now supported if possible (that is, if [ssl.HAS_SNI](https://docs.python.org/3/library/ssl.html#ssl.HAS_SNI) is true).   
_New in version 3.2:_ _data_ can be an iterable object.  
_Changed in version 3.3:_ _cadefault_ was added.  
_Changed in version 3.4.3:_ _context_ was added.  

#####<a id="Request">_class urllib.request.Request(url, data=None, headers={}, origin_req_host=None, unverifiable=False, method=None)_</a>

This class is an abstraction of a URL request.  
这个类是一个关于URL请求的抽象.  

—_url_ should be a string containing a valid URL.  
_url_应该包含一个有效的URL字符串.  

_data_解释与_urllib.request.openurl()_部分相同,点[这里!!]()查看详细介绍.  

_headers_ should be a dictionary, and will be treated as if [add_header()](https://docs.python.org/3/library/urllib.request.html#urllib.request.Request.add_header) was called with each key and value as arguments. This is often used to “spoof” the `User-Agent` header, which is used by a browser to identify itself – some HTTP servers only allow requests coming from common browsers as opposed to scripts. For example, Mozilla Firefox may identify itself as `"Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11"`, while [urllib](https://docs.python.org/3/library/urllib.html#module-urllib)‘s default user agent string is `"Python-urllib/2.6"` (on Python 2.6).  
_headers_应该是一个dictionary,使用它就像以每个key and value作为说明调用[urllib.request.Request.add_header()!!]()一样.它经常被用来“欺骗”被浏览器用作识别本身的`User-Agent`头——一些HTTP服务器仅允许来自相对于脚本来说的普通浏览器请求.例如,Mozilla Firefox可以使用`"Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11"`识别自己,然而`urllib`默认的user agent字符串是`"Python-urllib/2.6"`(on Python2.6).  

An example of using `Content-Type` header with _data_ argument would be sending a dictionary like `{"Content-Type":" application/x-www-form-urlencoded;charset=utf-8"}`.  
一个使用带有_data_说明的`Content-Type`头例子将发送一个像这样`{"Content-Type":" application/x-www-form-urlencoded;charset=utf-8"}`的字典.  

The final two arguments are only of interest for correct handling of third-party HTTP cookies:  
_origin\_req\_host_ should be the request-host of the origin transaction, as defined by [RFC 2965](http://tools.ietf.org/html/rfc2965.html). It defaults to `http.cookiejar.request_host(self)`. This is the host name or IP address of the original request that was initiated by the user. For example, if the request is for an image in an HTML document, this should be the request-host of the request for the page containing the image.  
最后两点说明是正确操作第三方HTTP cookies的注意项:  
_origin\_req\_host_应该是the request-host of the origin transaction,在[RFC 2965](http://tools.ietf.org/html/rfc2965.html)中定义.它默认为`http.cookiejar.request_host(self)`.这是先前由用户发起的原请求的主机名或IP地址.例如,如果该请求是针对HTML文档中的图像,这应该是包含图像的网页请求的request-host机为.  

_unverifiable_ should indicate whether the request is unverifiable, as defined by RFC 2965. It defaults to `False`. An _unverifiable_ request is one whose URL the user did not have the option to approve. For example, if the request is for an image in an HTML document, and the user had no option to approve the automatic fetching of the image, this should be true.  
_unverifiable_表明该请求是否是无法核实的,在RFC 2965中定义.默认值为`False`.一个无法证实的请求是指其URL无法被使用者验证的.例如,如果该请求是针对HTML文档中的图像,并且用户无法自动抓取图像,它应该为True.  

_method_ should be a string that indicates the HTTP request method that will be used (e.g. `'HEAD'`). If provided, its value is stored in the [method](https://docs.python.org/3/library/urllib.request.html#urllib.request.Request.method) attribute and is used by [get_method()](https://docs.python.org/3/library/urllib.request.html#urllib.request.Request.get_method). Subclasses may indicate a default method by setting the [_method_](https://docs.python.org/3/library/urllib.request.html#urllib.request.Request.method) attribute in the class itself.  
_method_应该是一个说明使用哪种HTTP请求方法的字符串(例如,`'HEAD').如果提供该字符串,它的值被存储在[method!!]()属性中,并且被用于[get_method()!!]()函数.通过在类本身中设置[method!!]()属性,子类可以声明默认的方法.  

_Changed in version 3.3:_ [Request.method](https://docs.python.org/3/library/urllib.request.html#urllib.request.Request.method) argument is added to the Request class.

_Changed in version 3.4_: Default [Request.method](https://docs.python.org/3/library/urllib.request.html#urllib.request.Request.method) may be indicated at the class level.
