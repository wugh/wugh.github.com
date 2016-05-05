title: CS224d笔记4续——RNN隐藏层计算之GRU和LSTM
date: 2016-03-13 21:22
category: NLP
tags: 神经网络,RNN,循环神经网络,深度学习,GRU,LSTM
slug: cs224d-notes4-recurrent-neural-networks-continue
---

本篇文章主要介绍两种RNN的隐藏层信息计算方法GRU（Gated Recurrent Units）和
LSTM（Long-Short-Term-Memories），这两种隐藏层的计算方法通过引入门（Gate）
的机制来解决RNN的梯度消失问题，从而学习到长距离依赖。

这里说的隐藏层计算方法指的是如何计算下个时刻的隐藏层信息，标准RNN中计算
方法是：
$$h_t=f(W^{(hh)}h_{t-1}+W^{(hx)}x_t)$$
而LSTM和GRU可以理解为计算$h_t$的另一种方法。


## LSTM

[这篇文章][lstm]详细 地解释了LSTM各个门的物理含义，
以及LSTM计算隐藏层的方法，这里简要的进行总结，
下图是LSTM网络的示意图，图中各个符号的含义参考[原文][lstm]：
![LSTM RNN]({filename}/images/NLP/rnn-lstm-chain.png){: style="display:block;margin:0 auto"}

某个时刻LSTM计算隐藏层的方法参考下图：
![LSTM 单元]({filename}/images/NLP/rnn-lstm-unit-detail.png){: style="display:block;margin:0 auto"}

LSTM最核心的部分是`cell state`，即图中的$c_t$。$c_t$的信息贯穿整个LSTM，
在整个前向传播的过程中只在$c_t$上进行一些简单的线性操作，通过门来控制
$c_t$中信息的增减。LSTM中的门是通过一个sigmoid层来实现的，门输出的数值在
0~1之间，然后把门的取值向量和目标数据对应维相乘就可以达到控制数据流通的
效果。LSTM中有三个门，分别是`forget gate`、`input gate`和`output gate`，
这三个门的计算方法公式一样，都是根据$x_t$和$h_{t-1}$来计算，
区别在于权重矩阵和偏置不同。

1. 首先是`forget gate`$f_t$，这个门主要控制要从`cell state`中忘记哪些信息，计算方法如下:
$$f_t=\sigma(W^fx_t+U^fh_{t-1})$$
2. 其次是`input gate`$i_t$，这个门控制当前时刻的新信息（candidate hidden layer）有哪些需要添加进`cell state`中，计算方法如下:
$$i_t=\sigma(W^ix_t+U^ih_{t-1})$$
3. 上一步提到的当前时刻新信息的计算方法如下：
$$\tilde{c}_t=\tanh(W^cx_t+U^ch_{t-1})$$
4. 然后$t$时刻`cell state`中的信息就变成$c_{t-1}$中的部分信息再叠加上$\tilde{c}_t$中的部分信息，计算方法如下：
$$c_t=f_t\circ c_{t-1} + i_t\circ\tilde{c}_t$$
5. 最后还需要根据$t$时刻的`cell state`输出$h_t$，通过`output gate`来控制`cell state`中的哪些信息需要
输出，`output gate`的计算方法如下：
$$o_t=\sigma(W^ox_t+U^oh_{t-1})$$
将`cell state`中的信息经过一个$\tanh$层之后然后经过`output gate`过滤得到$h_t$：
$$h_t=o_t\circ\tanh(c_t)$$

如果我们把LSTM的`forget gate`全部置0（总是忘记之前的信息），`input gate`全部
置1，`output gate`全部置1（把`cell state`中的信息全部输出），这样LSTM就变成一个标准的RNN。
[上文提到的文章][lstm]中还提到一些LSTM的变种，比如根据$h_{t-1}$、$x_t$和$c_t$来计算门信息。

## GRU

GRU可以看成是LSTM的变种，GRU把LSTM中的`forget gate`和`input gate`用`update gate`来替代。
把`cell state`和隐状态$h_t$进行合并，在计算当前时刻新信息的方法和LSTM有所不同。
下图是GRU更新$h_t$的过程：
![GRU]({filename}/images/NLP/rnn-gru-unit.png){: style="display:block;margin:0 auto"}
具体更新过程如下：

1. 首先介绍GRU的两个门，分别是`reset gate`$r_t$和`update gate`$z_t$，计算方法和LSTM中
门的计算方法一致：
$$\begin{align*}
r_t&=\sigma(W^rx_t+U^rh_{t-1})\\
z_t&=\sigma(W^zx_t+U^zh_{t-1})
\end{align*}$$
1. 其次是计算候选隐藏层（candidate hidden layer）$\tilde{h}_t$，这个候选隐藏层
和LSTM中的$\tilde{c}_t$是类似，可以看成是当前时刻的新信息，其中$r_t$用来控制需要
保留多少之前的记忆，如果$r_t$为0，那么$\tilde{h}_t$只包含当前词的信息：
$$\tilde{h}_t=\tanh(Wx_t+r_tUh_{t-1})$$
1. 最后$z_t$控制需要从前一时刻的隐藏层$h_{t-1}$中遗忘多少信息，需要加入多少当前
时刻的隐藏层信息$\tilde{h}_t$，最后得到$h_t$，直接得到最后输出的隐藏层信息，
这里与LSTM的区别是GRU中没有`output gate`：
$$h_t=z_t\circ h_{t-1} + (1-z_t)\circ \tilde{h}_t$$

如果`reset gate`接近0，那么之前的隐藏层信息就会丢弃，允许模型丢弃一些和未来无关
的信息；`update gate`控制当前时刻的隐藏层输出$h_t$需要保留多少之前的隐藏层信息，
若$z_t$接近1相当于我们之前把之前的隐藏层信息拷贝到当前时刻，可以学习长距离依赖。
一般来说那些具有短距离依赖的单元`reset gate`比较活跃（如果$r_t$为1，而$z_t$为0
那么相当于变成了一个标准的RNN，能处理短距离依赖），具有长距离依赖的单元`update gate`比较活跃。

LSTM和RNN的`theano`实现可以参考[这篇文章][grulstm]。

[lstm]: https://colah.github.io/posts/2015-08-Understanding-LSTMs/
[grulstm]: http://www.wildml.com/2015/10/recurrent-neural-network-tutorial-part-4-implementing-a-grulstm-rnn-with-python-and-theano/
