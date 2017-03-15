#HTTPResponse Objects

An [HTTPResponse](https://docs.python.org/3/library/http.client.html#http.client.HTTPResponse) instance wraps the HTTP response from the server. It provides access to the request headers and the entity body. The response is an iterable object and can be used in a with statement.  
一个包含HTTP相应的_HTTPResponse_实例. 它提供了访问request headers与entity body的方法. 这个响应是一个可迭代对象，and can be used in a with statement.  

#####_HTTPResponse.read([amt])_  
Reads and returns the response body, or up to the next _amt_ **bytes**.  

#####_HTTPResponse.readinto(b)_  
Reads up to the next len(b) bytes of the response body into the buffer _b_. Returns the number of bytes read.  
_New in version 3.3._

#####_HTTPResponse.getheader(name, default=None)_  
Return the value of the header _name_, or _default_ if there is no header matching _name_. If there is more than one header with the name _name_, return all of the values joined by ‘,‘. If ‘default’ is any iterable other than a single string, its elements are similarly returned joined by commas.  

#####_HTTPResponse.getheaders()_  
Return a list of (header, value) tuples.  
返回(header, value)元组形式的列表.  

#####_HTTPResponse.fileno()_  
Return the `fileno` of the underlying socket.  

#####_HTTPResponse.msg_  
A _http.client.HTTPMessage_ instance containing the response headers. _http.client.HTTPMessage_ is a subclass of [email.message.Message](https://docs.python.org/3/library/email.message.html#email.message.Message).  

#####_HTTPResponse.version_  
HTTP protocol version used by server. 10 for HTTP/1.0, 11 for HTTP/1.1.  

#####_HTTPResponse.status_  
Status code returned by server.  

#####_HTTPResponse.reason_  
Reason phrase returned by server.  

#####_HTTPResponse.debuglevel_  
A debugging hook. If [debuglevel](https://docs.python.org/3/library/http.client.html#http.client.HTTPResponse.debuglevel) is greater than zero, messages will be printed to stdout as the response is read and parsed.  

#####_HTTPResponse.closed_  
Is `True` if the stream is closed.  

====
```
2015 11.1 下午
```
