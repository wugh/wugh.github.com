title: CS224d笔记3——神经网络
date: 2016-03-01 09:00
category: NLP
tags: 神经网络,后向传播,bp算法
slug: cs224d-notes3-neural-networks-and-backward-propagation
---

这部分首先介绍神经元，接着介绍只有一个隐藏层的神经网络，这个神经网络要解决的
问题和[上一篇文章]({filename}/NLP/cs224d-notes2.md)类似，这里对窗口分类任务进一步
简化，我们只需要判断中心词是否为地点。利用这个简单的神经网络说明前向传播和
后向误差传播算法，然后推出通用的后向误差传播算法。最后介绍一些神经网络在工程
实现中的一些技巧。

## 神经元

神经元是组成神经网络的基础单元，神经元通常接受$n$个输入产生一个输出，运算过程如下图：
![神经元]({filename}/images/NLP/neural-network-neuron.png){: style="display:block;margin:0 auto"}
神经元的参数包括一个$n$维的权重向量$w$和一个偏置$b$（$b$为标量），偏置可以看成判断类别的先验，
神经元的输出为$h{w,b}(x)=f(w^Tx + b)$，$f$被成为“激活函数”。本文默认使用的激活函数为sigmoid函数
（用符号$\sigma$表示）：
$$f(z)=\sigma(z)=\frac{1}{1+\exp(-z)}$$
更多的激活函数将在后文讨论，这里不再展开，需要注意的是sigmoid函数的求导结果为
$$\sigma'(z)=\sigma(z)(1-\sigma(z))$$

## 单隐藏层神经网络

神经网络的特点在于把一个输入向量同时输入到一系列神经元，然后得到新的输出向量，
然后这个新的向量又可以作为下一层一系列神经元的输入，如下图所示：
![神经网络例子]({filename}/images/NLP/neural-network-3-layers-example.png){: style="display:block;margin:0 auto"}
我们使用圆圈来表示神经网络的输入，标上“+1”的圆圈被称为偏置节点，也就是截距项。
神经网络最左边的一层叫做输入层，最右的一层叫做输出层（本例中，输出层只有一个节
点）。中间所有节点组成的一层叫做隐藏层，因为我们不能在训练样本集中观测到它们的
值。同时可以看到，以上神经网络的例子中有3个输入单元（偏置单元不计在内），3个隐
藏单元及一个输出单元。本文使用的符号参考[UFLDL教程](ufldl)，计算隐藏层的过程如下图所示：
![神经网络记号]({filename}/images/NLP/neural-network-3-layers-example-notation.png){: style="display:block;margin:0 auto"}

## 前向计算

可以把神经网络应用于[上一篇文章]({filename}/NLP/cs224d-notes2.md)中提到的窗口分
类问题，这里我们主要只是为了用这个简单的神经网络说明前向计算和后向误差传播，所
以将任务限定为只需要判断中心词是否为地点，并且采用的网络只有一个隐藏层。
例如窗口内容为“meseums in Paris are amazing”，判断中心词“Paris”是否为地点，
假设词向量维度为4，那么窗口向量$x_{\text{window}}=x\in \mathbb{R}^{20}$，
隐藏层用8个神经元，然后用8个神经元的输出来计算得分，最后利用这个得分判断中心词是否为实体。
下图为计算$\text{score(meseums in Paris are amazing)}$的示意图，
从输入逐层向输出层传播最后得到输出的过程成为前向传播：
![前向计算]({filename}/images/NLP/neural-network-3-layers-ner-forward-computation.png){: style="display:block;margin:0 auto"}
通过非线性的隐藏层可以学习到词向量之间的非线性关系来帮助分类任务，例如“第一个词是‘meseums’
并且第二个词是‘in’"可以帮助判断第三个词是否为地点。

## Max-margin目标函数

本文的窗口分类任务将使用Max-margin目标函数，Max-margin的思想是使得网络在“正确”
记作$s$，数据点上的得分大于“错误”数据点上的得分记作$s_c$（c代表corrupt），在窗
口分类任务中“正确”数据点指的是中心词为地点的窗口例如“meseums in Paris are amazing”，
“错误”数据点指的是中心词非地点的窗口例如“not all meseums in Paris”。

我们的优化目标就变成$\text{maxmize}(s-s_c)$或者$\text{minimize}(s_c-s)$，
这里对优化目标进行修改，只有当$s_c>s$即$s_c-s>0$时才计算梯度更新参数，主要思想是我们
比较关心那些“错误”数据点得分大于“正确”样本点的数据对，优化目标变成下面形式：
$$\text{minimize}J=\max(s_c-s,0)$$
上述的目标生成的边缘不够安全，我们希望最后正确样本点的得分$s$比任意错误样本点的得分高出一个正数$\Delta$。
所以我们希望对于$s-s_c<\Delta$即$s_c+\Delta-s>0$的正负样本对计算梯度，如果取$\Delta=1$可以得到下面的优化目标：
$$\text{minimize}J=\max(1+s_c-s,0)$$
其中$s=U^Tf(Wx+b)$，$s_c=U^Tf(Wx_c+b)$。

## 后向传播（链式法则）

有了目标函数之后，优化神经网络的关键在于如何对$J$求每个参数的导数。在我们的三层网络中参数有
$U$，$W$，$b$，$x$。假设$J=(1+s_c-s)>0$，可得：
$$\frac{\partial J}{\partial s}=-\frac{\partial J}{\partial s_c}=-1$$
所以我们只要关心$s$对于$U$，$W$，$b$，$x$的导数，求导过程中需要用到链式法则
$\frac{\partial y}{\partial x}=\frac{\partial y}{\partial u}\frac{\partial u}{\partial x}$。

首先是$s$对$U$求导，由于$s=U^Ta=U^Tf(z)=U^Tf(Wx+b)$，所以：
![s对U求导]({filename}/images/NLP/neural-network-3-layers-ner-derivate-wrt-U.png){: style="display:block;margin:0 auto"}

考虑$s$对于$W_{ij}$的导数，由前向传播过程可知$W_{ij}$只在计算$a_i$的过程中使用，例如下图说明了$W_{23}$只在计算$a_2$的时候用到：
![网络示意图]({filename}/images/NLP/neural-network-3-layers-ner-graph.png){: style="display:block;margin:0 auto"}
所以导数计算过程如下：
![s对W求导]({filename}/images/NLP/neural-network-3-layers-ner-derivate-wrt-W.jpg){: style="display:block;margin:0 auto"}
需要注意这个求导过程中我们将$s$对于$z$的导数记作$\delta=U\circ f'(z)$，这个将在后面的求导过程中反复用到。

考虑$s$对于$b_i$的导数，计算过程与$W_{ij}$的导数类似：
\begin{align*}
\frac{\partial s}{\partial W_{ij}}&=\frac{\partial s}{\partial a_i}\frac{\partial a_i}{\partial z_i}\frac{\partial z_i}{\partial b_i}\\
&=U_if'(z_i)\frac{\partial (W_{i\cdot}x+b_i)}{b_i}\\
&=\delta_i
\end{align*}
所以$s$对于$b_i$的导数为$\delta$。

现在考虑$s$对于$x_j$的导数，由于每个$a_i$都和特定的$x_j$相连，所以$x_j$会影响所有隐藏层的输出，求导过程如下：
![s对x求导]({filename}/images/NLP/neural-network-3-layers-ner-derivate-wrt-x.png){: style="display:block;margin:0 auto"}
所以$s$对于$x$的导数为$W^T\delta$。

## 后向传播（误差传播）

下面从误差（error）后向传播的角度来解释$s$对于$W_{ij}^{(1)}$的梯度。$W^{(k)}$为第$k$层和第$k+1$层之间的权重矩阵，
图中$W^{(1)}$等价于上文提到的$W$，$W^{(2)}$等价于上文提到的$U$。$b_j^{(k)}$为第$k+1$层第j个神经元的偏置，
图中的$b^{(1)}$等价于上文提到的$b$。下图中$a_j^{(k)}$表示第k层第j个神经元的输出，
下图中$z_j^{(k)}$表示第k层第j个神经元的标量输入。
![神经网络符号说明]({filename}/images/NLP/neural-network-3-layers-bp-symbol.jpg){: style="display:block;margin:0 auto"}
$\delta_1^{(2)}$表示传播到$z_1^{(2)}$位置的误差，即$s$相对于$z_1^{(2)}$的导数，如下图：
![delta含义]({filename}/images/NLP/neural-network-3-layers-bp-delta.png){: style="display:block;margin:0 auto"}

下图说明了如何利用反向误差来计算$W_{12}^{(1)}$处的误差：
![误差传播]({filename}/images/NLP/neural-network-3-layers-bp-error-w12.jpg){: style="display:block;margin:0 auto"}
可知最后$W_{12}^{(1)}$处的误差为$\delta_1^{(2)}a_2^{(1)}$，那么对于整个矩阵$W^{(1)}$的误差可以写成${\delta^{(2)}}^Ta^{(1)}$。
可以看出反向误差传播本质上也是链式法则，不过看起来更直观，下面总结了反向误差传播的两个要点：

1. 误差$x$向后传播穿过一个神经元时只需要将误差乘以当前神经元的局部梯度，如下图
![误差传播]({filename}/images/NLP/neural-network-3-layers-bp-delta-neuron.png){: style="display:block;margin:0 auto"}
1. 误差$\delta$沿着线性变换后向传播时，只需要将误差乘以前向传播时的对应线性变换权重，如下图（绿色为前向，黄色为后向）
![误差传播]({filename}/images/NLP/neural-network-3-layers-bp-delta-affine.png){: style="display:block;margin:0 auto"}

整个后向传播过程可以看出我们定义的$\delta^{(k)}$在计算误差的过程中十分重要，
需要知道如何从$\delta^{(k)}$计算$\delta^{(k-1)}$，即如何把$z^{(k)}$处的误差传播到$z^{(k-1)}$，
现在先考虑如何得到$z_j^{(k-1)}$处的误差：
![误差传播]({filename}/images/NLP/neural-network-3-layers-bp-delta-to-delta.png){: style="display:block;margin:0 auto"}

1. 对于第k层特定的$z_i^{(k)}$处的误差首先需要传播到$a_j^{(k-1)}$位置，在前向计算时从$a_j^{(k-1)}$到
$z_i^{(k)}$是线性变换，所以$a_j^{(k-1)}$从$z_i^{(k)}$处接收到的误差为$\delta_i^{(k)}W_{ij}^{(k-1)}$
1. 由于第k层每个$z_i^{(k)}$处的误差都会传播到$a_j^{(k-1)}$位置（层与层之间全连接），
所以$a_j^{(k-1)}$从所有的$z_i^{(k)}$处收到的总误差为$\sum_i \delta_i^{(k)}W_{ij}^{(k-1)}$
1. 可以看到从$z_j^{(k-1)}$到$a_j^{(k-1)}$穿过了一个神经元，所以$a_j^{(k-1)}$处的误差传播到$z_j^{(k-1)}$
时需要乘以这个神经元的局部梯度$f'(z_j^{(k-1)})$，得到$z_j^{(k-1)}$处的误差$\delta_j^{(k-1)}$
为$f'(z_j^{(k-1)})\sum_i \delta_i^{(k)}W_{ij}^{(k-1)}$

根据$\delta_j^{(k-1)}=f'(z_j^{(k-1)})\sum_i \delta_i^{(k)}W_{ij}^{(k-1)}$，
从$\delta^{(k)}$计算$\delta^{(k-1)}$的过程可以写成矩阵形式：
$$\delta^{(k-1)}=f'(z^{(k-1)})\circ({W^{(k-1)}}^T\delta^{(k)})$$

## Tips和Tricks

剩下部分将讨论一下神经网络在工程首先中的一些技巧。

### 神经网络的使用策略

1. 选择适当的网络结构
	1. 结构：单个词，固定窗口，词袋，递归 vs 循环，CNN，基于句子 vs 基于文档
	1. 非线性函数选择
1. 用梯度检查来校验是否有实现bug
1. 参数初始化
1. 优化技巧
1. 检查模型是否能够在数据集上过拟合
	1. 如果不能，那么需要改变模型结果或者让模型参数规模更大（例如增加隐藏层）
	1. 如果可以，那么增加正则化项

### 神经元非线性函数选择

最常用的两个非线性函数是sigmoid和tanh函数，tanh可以看成对sigmoid函数进行了缩放和平移
$$\tanh(z)=2\sigma(2z)-1$$
sigmoid和tanh的函数图像和导数形式如下：
![sigmoid和tanh]({filename}/images/NLP/neural-network-tricks-non-linearities.png){: style="display:block;margin:0 auto"}
tanh函数在深度网络中的表现通常要比sigmoid好，这里还有一些额外的非线性函数，
其中[ReLu函数][relu]在2015年成为了深度神经网络最受欢迎的非线性函数。
![更多的非线性函数]({filename}/images/NLP/neural-network-tricks-non-linearities-more.png){: style="display:block;margin:0 auto"}

### 梯度检查（Gradient Check）

前文描述的后向算法采用使用微积分来计算偏导数，但是其实我们可以根据导数的定义，
采用数值方法来估计偏导数，检查过程如下：

1. 实现前向计算和后向误差传播
2. 对于网络中的每一个参数（假设记作$\theta$，$\theta$包含了网络所有的$W$，$b$），
然后按下列公式计算$\theta$每一维的梯度，$h$一般取一个较小的数（例如0.00001）：
![梯度检查]({filename}/images/NLP/neural-network-tricks-non-gradient-check.png){: style="display:block;margin:0 auto"}
3. 对比后向误差传播计算的梯度和第2步计算的梯度是否很接近

### 参数初始化

把偏置初始化成0，然后权重矩阵的初始化方式如下：
$$W^{(l)}\sim U\left[-\frac{\sqrt{6}}{\sqrt{n^{(l)} + n^{(l+1)}}},\frac{\sqrt{6}}{\sqrt{n^{(l)}+n^{(l+1)}}}\right]$$
其中$n^{(l)}$表示第$l$层的神经元个数，$n^{(l+1)}$表示第$l+1$层的神经元个数。

### 学习率

随机梯度下降一般在一个或者数个样本（mini-batch）上计算梯度，然后进行参数更新，
最简单的随机梯度下降采用固定的学习率$\alpha$，学习率不能设置太大：
![固定的alpha]({filename}/images/NLP/neural-network-tricks-learning-rate-fixed-alpha.png){: style="display:block;margin:0 auto"}

较好的方法是让学习率随着迭代次数$t$逐步下降：
![alpha随时间下降]({filename}/images/NLP/neural-network-tricks-learning-rate-decrease-alpha.png){: style="display:block;margin:0 auto"}
其中$\alpha(0)$表示初始的学习率是一个可调参数，$\tau$是另一个参数表示从何时开始学习率开始降低。
在实践中，这种方法取得的结果通常不错。

下面将讨论一种不需要手工设定学习率的方法，称之为Adagrad，这种方法的特点在于每个参数使用的学习率都不同。

### Adagrad

不同参数使用不同的学习率，越少进行更新的参数采用的学习率大于那些更新频繁的参数，具体每个参数的学习率变化如下：
![adagrad]({filename}/images/NLP/neural-network-tricks-adagrad.png){: style="display:block;margin:0 auto"}

### 正则化（Regularization）

当我们的模型在训练集上过拟合之后，需要对模型进行正则化，一般来说是将权重矩阵的$L_2$正则项加入损失函数（偏置不加入）：
![L2正则]({filename}/images/NLP/neural-network-tricks-regularization.png){: style="display:block;margin:0 auto"}
其中${\Vert W^{(i)}\Vert}_F$称为弗罗贝尼乌斯范数（Frobenius norm）：
![弗罗贝尼乌斯范数]({filename}/images/NLP/neural-network-tricks-matrix-F-norm.png){: style="display:block;margin:0 auto"}
可以看出正则项会惩罚大的参数，$\lambda$是超参（越大则越认为$W$应该接近0），加入$L_2$正则项之后会使得$W$接近0，
使得网络拟合的目标函数灵活性降低从而避免过拟合。
防止过拟合的方法除了加入正则项之外，还有`Early Stopping`（根据模型在发展集上的性能停止训练）。

### 防止特征共同适应（Co-adaptation）

特征Co-adaptation指的是某个特征只有在另个特征出现时才有用。防止特征
Co-adaptation的方法是Dropout，顾名思义就是在训练模型的时候随机扔掉一部分的输入
（即随机把一部分输入变成0）
$$a^{(k+1)}=f\left (W^{(k)}(r\circ a^{(k)})+b\right )$$
$p$为超参，其中$r$的每一维以概率$p$置成1，以$1-p$的概率置成0。测试的时候不需要Dropout，
采用Dropout可以也防止模型对于特定的特征共现过拟合。

[ufldl]: http://ufldl.stanford.edu/wiki/index.php/%E7%A5%9E%E7%BB%8F%E7%BD%91%E7%BB%9C
[relu]: https://en.wikipedia.org/wiki/Rectifier_(neural_networks)
