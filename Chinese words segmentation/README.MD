# 中文分词
## 作业提示
- This task provides PKU data as training set and test set (e.g., you can use 80% data for model training and other 20% for testing ), and you are free to use data learned or model trained from any resources.
- Evaluation Metrics:
  * Precision = (Number of words correctly segmented)/(Number of words segmented) * 100%
  * Recall = (Number of words correctly segmented)/(Number of words in the reference) * 100%
  * F measure = 2*P*R / (P+R)
## 任务定义
将语料库“1998-01-105-带音.txt”进行预处理，前 80%行将分好的词作为训练集，后 20%连成句子作为测试集；   
对于每一个句子，可以根据训练集的词库输出一种分词结果，例如：原句: 我今天很开心 分词结果：我/今天/很/开心；  
将分词结果与该句子标准分词结果对比，计算准确率 precision、召回率 recall 和 F-measure 三个参数，并将分词结果输出。
## 开发环境
- 开发平台：`Windows 10 + Python 3.6`
- IDE：`PyCharm Community Edition 2017.2.4`
## 输入、输出
- 输入：“1998-01-105-带音.txt”，为命名简便已改为“123.txt”
- 输出：
      * 每一行应分为的词数、程序分成的词数、分对的词数，以及标准分法和该程序的分
法，输出到屏幕以及“result.txt”。
      * 整个测试集的总词数、程序分成的总词数、正确率、召回率和 F-measure，输出到
屏幕和“result.txt” 
## 运行结果
- 应分为212884个词，程序分为了222803个词，分对了199072个词
- 正确率：0.893  召回率：0.935  F-measure：0.913
- 程序运行时间：5秒04
