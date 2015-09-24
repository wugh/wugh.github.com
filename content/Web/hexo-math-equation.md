title: hexo数学公式
date: 2013-11-12 12:20:30
category: Web
tags: latex, vim, hexo
slug: hexo-math-equation
---

在使用[Hexo](https://github.com/tommy351/hexo "Hexo")写博客的时候无法插入数学公
式，通过调研发现[MathJax](http://www.mathjax.org/ "MathJax")可以很好的在网页里
面显示数学公式，并且能够支持很多浏览器，下面分步骤描述生成公式的方法。

### 修改主题
MathJax的[官方文档](http://docs.mathjax.org/en/latest/platforms/index.html)说只
要在每个页面的`head`标签里面插入下面的`javascript`代码：
```html 
<script type="text/javascript"
   src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML"></script>
```
接下来的步骤就是要把这个代码加入所有的文章页面里面，这里参考
[greyshade](https://github.com/nuklly/hexo-theme-greyshade "hexo theme
greyshade")中对这段代码的处理方式，在主题目录`themes/light/layout/_partial/`下
新建一个文件`mathjax.ejs`，内容如下：
```html
<!-- mathjax config similar to math.stackexchange -->

<script type="text/x-mathjax-config">
  MathJax.Hub.Config({
    tex2jax: {
      inlineMath: [ ['$','$'], ["\\(","\\)"] ],
      processEscapes: true
    }
  });
</script>

<script type="text/x-mathjax-config">
    MathJax.Hub.Config({
      tex2jax: {
        skipTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code']
      }
    });
</script>

<script type="text/x-mathjax-config">
    MathJax.Hub.Queue(function() {
        var all = MathJax.Hub.getAllJax(), i;
        for(i=0; i < all.length; i += 1) {
            all[i].SourceElement().parentNode.className += ' has-jax';
        }
    });
</script>

<script type="text/javascript" src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML">
</script>
```

然后在`themes/light/layout/_partial/`目录下的`head.ejs`里面添加以下几行：
```
<% if(theme.mathjax) {%>
    <%- partial('mathjax')%>
<% } %>
```

这几行的意思是如果在主题的`_config.xml`里面把`mathjax`变量设置成`true`那么就把
`mathjax.ejs`包含进来，所以还需要在`themes/_config.xml`里面添加：
```
mathjax: true
```
配置完之后生成的网页里面都包含有`mathjax`需要的一段`script`。

### 生成公式
有些`MarkDown`渲染器本来支持，例如
[kramdown](https://github.com/gettalong/kramdown "kramdown")。但是这个是`Ruby`
写的，`Hexo`无法支持，`Hexo`官方的`MarkDown`渲染器也无法对公式进行处理，现在
还可以采用[hexo pandoc render](https://github.com/wzpan/hexo-renderer-pandoc)
来进行渲染

#### 行间公式
要产生行间公式就得用下面的代码：
```latex
$E=mc^2$
```
现在举一个行间公式的例子：
```latex
爱因斯坦提出了质能方程：$E=mc^2$。他是一个伟大的物理学家。
```
爱因斯坦提出了质能方程：$E=mc^2$。他是一个伟大的
物理学家。

#### 方程组
我们可以用下面的一段代码来产生一个独立的方程组，由于一般`Markdown`中`\\`需要转义
，所以换行我们可以使用`\cr`
```latex
以下是几个三角恒等式：
$$
\begin{align}
\sin \left(x+y\right)=\sin x \cos y + \cos x \sin y\cr
\cos \left(x+y\right)=\cos x \cos y - \sin x \sin y
\end{align}
$$
```

以下是几个三角恒等式：
$$
\begin{align}
\sin \left(x+y\right)=\sin x \cos y + \cos x \sin y\cr
\cos \left(x+y\right)=\cos x \cos y - \sin x \sin y
\end{align}
$$

### vim插入模板
上述方法插入公式的时候总是要时间去敲很多没有意义的`html`标签，我们可以利用`vim`
的[vim-snipmate](https://github.com/garbas/vim-snipmate "snipmate")插件来做几个
模板加速我们的程序编写。
我写了两个`snippets`来插入公式：
```snippets
snippet $
    $${1:Inline}$${0}

snippet $$
    $$  ${1:Displayed}
    $$  
    ${0}
```
把这个`mkd.snippets`文件放到`~/.vim/snippets/`目录下面就可以生效，然后我们在编
辑`MarkDown`文件的时候就可以通过`$<Tab>`来触发一个行间公式模板，通过`$$<Tab>`来
生成方程组模板。
