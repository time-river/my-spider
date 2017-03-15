正则表达式的一个错误现象
```
原re规则    pattern = re.compile('<div.*?author">.*?<a.*?<img.*?>(.*?)</a>.*?<div.*?content">(.*?)<!--(.*?)-->.*?</div>(.*?)<div class="stats.*?class="number">(.*?)</i>',re.S)
错误的一版本   pattern = re.compile(r'<div.*?class="author.*?>.*?<a.*?href.*?title="(.*?)">.*?</a>.*?<div.*?class="content">(.*?)<!--(.*?)-->', re.S)
错误的另一个版本    pattern = re.compile(r'<div.*?class="author.*?>.*?<a.*?href.*?title="(.*?)">.*?</a>.*?<div.*?class="content">(.*?)<!--(.*?)-->.*?/div>.?*<div.*?class="stats.*?class="number">(.*?)</i>', re.S)
错误表现：运行findall()后无结果

需要匹配的部分code，匹配内容: 发布人、段子内容、点赞数

<div class="article block untagged mb15" id='qiushi_tag_113841240'>

<div class="author clearfix">
<a href="/users/11847517" target="_blank" rel="nofollow">
<img src="http://pic.qiushibaike.com/system/avtnew/1184/11847517/medium/20151109141612.jpg" alt="十字路口3"/>
</a>
<a href="/users/11847517" target="_blank" title="十字路口3">
<h2>十字路口3</h2>
</a>
</div>


<div class="content">

别人借钱不好意思拒绝，别人不还不好意思要  有过经历点赞
<!--1447759580-->

</div>



<div class="stats">
<span class="stats-vote"><i class="number">23369</i> 好笑</span>
<span class="stats-comments">


<span class="dash"> · </span>
<a href="/article/113841240" data-share="/article/113841240" id="c-113841240" class="qiushi_comments" target="_blank">
<i class="number">312</i> 评论
</a>



</span>
</div>
<div id="qiushi_counts_113841240" class="stats-buttons bar clearfix">
<ul class="clearfix">
<li id="vote-up-113841240" class="up">
<a href="javascript:voting(113841240,1)" class="voting" data-article="113841240" id="up-113841240" rel="nofollow">
<i class="iconfont" data-icon-actived="&#xf0061;" data-icon-original="&#xf001f;">&#xf001f;</i>
<span class="number hidden">23851</span>
</a>
</li>
<li id="vote-dn-113841240" class="down">
<a href="javascript:voting(113841240,-1)" class="voting" data-article="113841240" id="dn-113841240" rel="nofollow">
<i class="iconfont" data-icon-actived="&#xf0020;" data-icon-original="&#xf0020;">&#xf0020;</i>
<span class="number hidden">-482</span>
</a>
</li>

<li class="comments">
<a href="/article/113841240" id="c-113841240" class="qiushi_comments" target="_blank" rel="nofollow">
<i class="iconfont" data-icon-actived="&#xf0062;" data-icon-original="&#xf001d;">&#xf001d;</i>
</a>
</li>

</ul>
</div>
<div class="single-share">
<!-- JiaThis Button BEGIN -->
<div class="jiathis_style">
<span class="jiathis_txt">分享到：</span>
<a href="###" class="jiathis_button_weixin" rel="external nofollow"></a>
<a href="###" class="jiathis_button_cqq" rel="external nofollow"></a>
<a href="###"class="jiathis_button_qzone" rel="external nofollow"></a>
<a href="###" class="jiathis_button_tsina" rel="external nofollow"></a>
<a href="###" class="jiathis_button_tieba" rel="external nofollow"></a>
<a href="http://www.jiathis.com/share" class="jiathis jiathis_txt jtico jtico_jiathis" target="_blank" rel="external nofollow"></a>
</div>
<!-- JiaThis Button END -->
</div>
<div class="single-clear"></div>
</div>
```
