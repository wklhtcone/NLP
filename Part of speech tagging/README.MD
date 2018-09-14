# 词性标注
## 作业提示
- This data set contains one month of Chinese daily which are segmented and POS tagged under Peking Univ. standard.
- Project ideas: 
   * Design a sequence learning method to predicate a POS tags for each word in sentences. 
   * Use 80% data for model training and other 20% for testing (or 5-fold cross validation to test learner's performance. So it could be interesting to separate dataset.)
## 任务定义
将语料库“1998-01-105-带音.txt”进行预处理，前80%行将分好的词作为训练集，后20%连成句子作为测试集。  
对于每一个分好词的句子，利用隐马尔可夫模型(HMM)中的维特比算法计算出一个与之对应的词性序列。  
例如：原句：北京/举行/新年/音乐会，词性标注结果： ns/v/t/n。将程序的词性标注结果与该句子标准词性标注结果比对，计算正确率，并将词性标注结果输出
## 开发环境
- 开发平台：`Windows 10 + Python 3.6`
- IDE：`PyCharm Community Edition 2017.2.4`
## 输入、输出
- 输入：“1998-01-105-带音.txt”，为命名简便已改为“123.txt”
- 输出：
    * 每一行句子的词性个数、计算正确的词性个数，标准分词序列以及该程序的分词序列，输出到屏幕以及“result.txt”。
    * 整个测试集的总词性数、程序计算对的总词性数以及正确率，输出到屏幕和“result.txt”
## 原理
- HMM（隐马尔可夫）模型
- 维特比算法
## 几个矩阵的说明
#### A（状态转移矩阵）：
词性字典tagging的长度为n，共n种词性，所以二维列表A是n*n的
A[x][y]表示从键值为x的词性转移到键值为y词性的概率
状态转移矩阵的值应一句一句的算，避免一句话最后一个词到后一句话第一个词的情况
#### B（发射矩阵）：
词性字典tagging的长度为n，共n种词性；词字典dictionary的长度为m，共m种词，所以二维列表B是n*m的
B[x][y]表示键值为x的词性是键值为y的词的概率
#### Pi（初始概率矩阵）：
词性字典tagging的长度为n，共n种词性，所以列表Pi是1*n的
Pi[x]表示一个句子的第一个词为键值为x的词性的概率
#### delta：
测试集test_library中某句话的长度为k，词性字典tagging的长度为n
所以二维列表delta是k*n的
delta[x][y]表示测试到该句第x+1个词时，以键值为y的词性结尾的最大概率
#### phi：
测试集test_library中某句话的长度为k，词性字典tagging的长度为n
所以二维列表phi是k*n的，用于回溯
phi[x][y]表示测试到该句第x+1个词时，以键值为y的词性结尾的最大概率时上一个词的词性
#### num：
词性字典tagging的长度为n，共n个词性，所以列表num是1*n的
num[x]表示键值为x的词性在测试库中出现的次数，是计算矩阵A、B各项概率的分母

## 运行结果
- 共212884个词，标注正确的个数为173254个，正确率为0.8138
- 程序运行时间：15分26秒
