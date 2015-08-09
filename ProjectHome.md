<h3>A text encrypt program use Python and pyqt，the core algorithm is 128bit DES</h3>
text-encrypt是一个使用Python和pyqt编写的简单、易用的文本加密软件，核心算法是128位DES

text-encrypt可以使用一个口令将一段文本加密为不可读的文本，也可以再通过原来的口令将加密得到的不可读文本解密为原始文本

text-encrypt对输入口令计算md5，然后将得到的md5值作为密钥使用，所以支持中文，英文，甚至标点符号作为口令，但是注意不要忘记了你的口令，因为加密的安全性由DES算法的数学安全性保证，如果你忘记了，尽管我是text-encrypt的作者，我也无法帮你恢复

另外，text-encrypt不会连接互联网，你可以放心的使用它

<img src='http://text-encrypt.googlecode.com/files/ui_3.png' />

<img src='http://text-encrypt.googlecode.com/files/ui_2.png' />


<b>下面是给程序员看的:</b>

本项目还包含一个子项目：<b>des_X2</b>

<b>des_X2</b>项目使用C语言实现了密钥长度为128bit的DES加密算法，提供了C语言下加解密的实例，并最终将相关算法编译成des\_X2.dll供其他程序调用。

<b>text-encrypt</b>本身即是通过调用des\_X2.dll来实现加解密，而不是用Python来实现DES算法。

<b>des_X2</b>提供使用GCC的makefile和使用VC的makefile

感谢星空灭绝同学在DES算法方面提供的帮助

注:<b>des_X2</b>相关代码在本项目svn的des\_X2目录下


