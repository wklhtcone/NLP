# 情感分析
## 作业提示
- Given text about movie reviews
- Can we detect sentiment, like whether a comment is 
  * Positive? 
  * Negative?
- Can we tell to what extent is a comment positive of negative?  
- Data:
  * 5331 positive snippets
  * 5331 negative snippets  
## 任务定义
将语料库“rt-polarity.pos”、” rt-polarity.neg”进行预处理，将它们的前80%行分好的词作为朴素贝叶斯模型数据统计的来源；  
对于它们后20%行的每个句子，可以输出一个情感判断：negative或postive,并输出；  
例如：原句: everything is off. 判断结果：negative，判断正确。  
最终统计positive测试集正确率、negative测试集正确率、总正确率并输出。

## 开发环境
- 开发平台：`Windows 10 + Python 3.6`
- IDE：`PyCharm Community Edition 2017.2.4`
## 输入、输出
- 输入： “rt-polarity.pos”、” rt-polarity.neg”
- 输出：
     * 每一行判断的情感：positive或negative，以及判断结果是否正确
     * positive测试集、negative测试集正确率，以及总正确率，输出到屏幕和“result.txt”
## 原理
- 朴素贝叶斯模型
## 运行结果
- positive库准确率为0.772，negative库准确率为0.797，两个库总准确率为0.784
- 程序运行时间：2分01秒
