title: Learning to Rank入门
date: 2016-10-20 09:37
category: NLP
tags: Learning to Rank
slug: learning-to-rank-an-introduction
---

下面主要是阅读刘铁岩老师的《Learning to Rank for Information Retrieval》的一些
学习笔记。Learning to Ranking指的是根据训练数据用机器学习模型来解决排序问题。很
多IR问题都可以看成是排序问题，例如文档检索、协同过滤、关键词抽取、定义查找，本
文主要以文档检索为例子来描述Learning to Rank。

## 传统IR模型

传统的IR模型可以分成两类，一类是query-dependent，另一类是query-independent。

query-dependent指的是检索的时候考虑query和doc之间的关心，衡量这个关系的不同方法
产生了不同的模型, 考虑doc和query的相关性:

1. Boolean model: 对doc中的term做倒排，然后query是一个boolean表达式，对取回来的
   文档集合做交集并集等等
2. Vector space model: 把doc和query都表示在一个统一的欧拉空间（每个term一个维度
   ），每一个维度的值一般可以是TF-IDF，然后计算cosine距离
3. LSI: 根据term和doc构建一个矩阵，矩阵里面的值可以是TF-IDF，然后进行矩阵分解，
   得到term和doc的向量表示，新来一个query之后转换成低维空间的向量计算和doc的
   cosine相似度
3. BM25: 计算query和doc相关性分的经典方法
4. 基于语言模型的方法: 利用语言模型预估P(q|d)的概率

不考虑doc和query的相关性的时候，更重要的是如何考虑一个文档的质量，可以用PageRank
衡量
$$PR(d_u)=\sum_{d_v\in B_u}\frac{PR(d_v)}{U(d_v)}$$

## IR基于位置的评估方法

对于一个query给定m个对应的文档$\left\{d_j\right\}_{j=1}^m$，有三种方式给出文档
和query的关系:

1. 给出每个doc和query的相关性分，一般有两级和多级的表示方法，相关性之间可以比较
1. 对于某个query给出文档之间的偏序关系，$l_{u,v}=1$表示u比v更相关
1. 直接给出这个query下m篇文档的排列顺序

评估方法:

1. MRR (Mean reciprocal rank): 对于query来说第一个相关文档的位置$r(q)$，那么$1/r(q)$就是这个query的MRR
1. MAP (Mean Average precision): 首先P(k)指的是排序列表中topk个位置的精度，对每个query求AveP取平均得到MAP
$$P(k)=\frac{\mbox{topk中相关的文档个数}}{k}$$
$$\operatorname{AveP} = \frac{\sum_{k=1}^n (P(k) \times \operatorname{rel}(k))}{\mbox{number of relevant documents}}$$
1. NDCG (Normalised Discounted cumulative gain): 给定排序列表后p位置的DCG如下
$$ \mathrm{DCG_{p}} = rel_{1} + \sum_{i=2}^{p} \frac{rel_{i}}{\log_{2}i}. $$
NDGC指的对$DCG_p$进行了归一化，把$DCG_p$除以了完全正确排序时的$DCG_p$
$$ \mathrm{nDCG_{p}} = \frac{DCG_{p}}{IDCG{p}}. $$
1. RC (Rank correlation): RC给出了两个完整排序列表的不一致性, 例如可以用
[Kendall rank correlation coefficient](https://en.wikipedia.org/wiki/Kendall_rank_correlation_coefficient)衡量

这些评估方法都是以单个query为基础来评估的，并且每个query在评估文档排列时都需要
考虑文档所处的位置。

## Learning to Rank

文中把利用机器学习技术来解决排序问题的方法称为Learning to Rank。一般的做法是给
定query和doc抽取特征和真是label，特征包括doc本身的特征(PageRank值，点击率等等)
，以及query和doc之间的相关性特征(BM25等)，然后用机器学习方法去学习如何从特征空
间映射到label的空间。这些机器学习方法大体上可以分成三类：pointwise，pairwise，
listwise。下面主要谈谈自己对这三种方法的理解，具体的参见参考文献。

### pointwise

pointwise方法比较简单粗暴，把当个doc和query的特征看成输入，然后以这个pair是否相
关为目标来训练数据。关心单个文档和特定query的相关性。最后按照模型的相关性得分输
出给文档排序，得到query下doc的排序。

pointwise按照模型输出空间的不同又可以分成三类：回归，分类，ordinal regression（
类似分类，但是在这种回归的学习目标是学习到目标空间的几个有序划分点，然后每一段代表
一个分类）。

回归方法最简单的理解就是把问题看成一个线性回归问题，那么对于输入向量$x$可以用以下$f(x)$拟合相关分:
$$f_w(x) = w_0 + w_1x_1 + w_2x_2 + \cdots + w_nx_n$$
损失函数可以采用square loss, y为真是相关性分：
$$L(f(x), y) = (y-f(x))^2$$

看成分类问题时可以把是否相关看成两个分类，如果数据是多分类标注时就看成n个分类来学习，
采用logistics regression，最大熵，SVM都可以很好的解决该分类问题。

pointwise存在的问题:

1. 训练过程只考虑了单篇文档，没有学习到两篇文档的相对关系
1. 没有考虑到IR中评估性能的两个方面，没有考虑到一个query对应多个文档、loss函数
   没有体现文档在排序列表中的位置

### pairwise

pairwise方法解决了pointwise方法存在的第一个问题（训练过程考虑文档的相对顺序，即
在这个query下某个doc1和doc2的相关性谁强）。关心特定query下两个文档之间的相对顺序。

pairwise的学习目标是要减少误分类的文档对，即数据给定的方式是$(q, d_1, d_2)$，然后
如果$d_1$比$d_2$相关那么label为1，否则label为-1。

pairwise的中有些方法的方法感觉可以分成两种类型，一种是hypothesis就是建模两个文档
之间的相对关系，假定两个文档$x_u$和$x_v$那么，$h(x_u,x_v)$直接建模这两个文档的相对关系；
第二种模式是hypothesis建模还是单个文档的分，然后再损失函数里面考虑两个文档的相对关系，
假设$f(x_u)$和$f(x_v)$分别为两个文档的分数，然后如果$f(x_u)>f(x_v)$表示u比v相关。
下面主要针对第二种模式给出一个经典算法RankNet。其他经典方法还有RankSVM。

在RankNet用$P_{u,v}$表示$x_u$比$x_v$更相关的概率，对于特定query $q$如果文档
$x_u$比$x_v$更相关，那么我们要学习$\bar{y}_{u,v}=1$，相反的时候我们希望
$\bar{y}_{u,v}=0$。基于上面描述的评分函数$f$，$P$可以写成如下形式：
$$P_{u,v}(f) = \frac{\exp(f(x_u)-f(x_v))}{1+\exp(f(x_u)-f(x_v))}$$

可以用交叉熵来作为损失函数:
$$L(f;x_u,x_v,y_{u,v}) = -y_{u,v}\log{P_{u,v}}(f)-(1-y_{u,v})\log{(1-{P_{u,v}}(f))}$$

评分函数可以用神经网络来建模，交叉熵可以求导，直接把梯度传递给神经网络就可以完成整个训练过程。

虽然pairwise在考虑了文档之间的相对顺序，但是还没有把文档在ranklist中的绝对位置考虑到损失里面，
而且没有考虑到多个文档同属于一个query这种性质。

### listwise

listwise方法可以分成两种，一种模型的输出空间是文档列表中每个文档的相关性分数，
这里介绍softrank；另一种是建模整个文档列表的排列顺序，这里介绍ListNet。

listwise方法的最大优势是损失函数直接近似于IR的评估指标（MAP，NDGC等），IR的评估
指标一般非连续不可导，一般采用以下的替代方案:

1. 用连续可微的指标来逼近IR指标, softrank, apprank
2. bound IR指标, $SVM^{\mbox{map}}$, $SVM^{\mbox{ndgc}}$, PermuRank
3. 优化complex objectives, AdaRank, RankGP

SoftRank在文档排序分中引入随机性，用NDCG的期望来逼近原始的NDCG分数。假设给定query $q$，
对应的文档集合是$\mathbf{x}={x_j}_{j=1}^m$，$x_j$的得分$s_j$不再当成一个确定值来用，而是
当做一个随机变量，$s_j$是一个均值为$f(x_j)$方差为$\sigma_s$（这个$f$可以用神经网络建模，
$sigma$是超参数）:
$$p(s_j)=N(s_j|f(x_j),\sigma_s^2)$$
文档$x_u$排的比$x_v$靠前的概率可以描述如下:
$$p_{u,v}=\int_0^\inf N(s|f(x_u)-f(x_v),2\sigma_s^2)ds$$
有了$p_{u,v}$之后可以用迭代的方式表示用特定文档处于排序列表某个位置的概率。假设
$x_j$已经存在于列表中，此时需要加入$x_u$，那么如果$x_u$比$x_j$靠前那么加入之后$x_j$位置后移一位，
否则$x_j$位置不变。$p_j^u(r)$表示$x_u$加入后$x_j$处于$r$位置的概率:
$$p_j^u(r)=p_j^{(u-1)}(r-1)p_{u,j}+p_j^{(u-1)}(r)(1-p_{u,j})$$
SoftRank通过计算NDCG@m的期望来作为目标函数，又称之为SoftNDCG，通过最大化目标函数来学习$f$:
$$\mbox{SoftNDCG}\triangleq \frac{1}{Z_m}\sum_{j=1}^m(2^{y_i}-1)\sum_{r=0}^{m-1}\eta(r)p_j(r)$$

ListNet首先根据评分函数给文档打分，$\mathbf{s}=\{s_j\}_{j=1}^m$其中$s_j=f(x_j$
，然后根据Luce model来定义任意文档排列$\pi$的概率:
$$P(\pi|\mathbf{s})=\Pi_{j=1}^m\frac{\varphi(s_{\pi^{-1}(j)})}{\sum_{u=j}^m \varphi(s_{\pi^{-1}(u)})}$$
$\pi^{-1}(j)$表示文档排列$\pi$中第j位置的文档，$\varphi$是转换函数可以是sigmoid、线性或者指数。
上述建模好了当前评分函数$f$下任意排列的概率分数，我们还需要给出真实的任意排列概率分数$P_y(\pi)$，
（如果真实的文档列表是按照相关性分数给出，那么可以直接用Luce model给出真实分布；如果给出的仅仅是个
排序好的列表那么可以用delta函数给出分布，或者把位置转换成一个分数之后再利用Luce model）。通过
计算两个分布的KL散度，可以建模损失函数:
$$L(f;\mathbf{x},\pi_y)=D_{\mathrm{KL}}(P(\pi|\varphi(f(w,\mathbf{x})))\| P_y(\pi))$$
ListNet在训练过程中要计算的KL散度计算复杂度和$m$呈指数关系，因为需要考虑所有排列。ListNet的
原始文献中进一步基于top-k luce model给出top-k版本的KL散度，把计算复杂度降低到$m$的多项式复杂度。

基于ListNet，提出了ListMLE，基本思想和ListNet很像。根据评分函数用luce model建模排列
的概率分布，把优化目标改成了最大化真实排列的最大似然概率:
$$L(f;\mathbf{x},\pi_y)=-\log P(\pi_y|\varphi(f(w,\mathbf{x})))$$
ListMLE的训练数据需要给定query对应的整个排序列表，如果数据按pairwise或者pairwise方式给出
要想办法转换成一个完整列表。
