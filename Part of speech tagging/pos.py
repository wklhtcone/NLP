#coding=utf-8
import re
import datetime
starttime=datetime.datetime.now()
m=0# m代表词库dictionary中词的种类数
n=0# n代表词性库tagging中词性的种类数
rows=0# 代表语料库中总行数
correct=0#词性匹配对的个数
current_correct=0#当前行匹配对的个数
total=0#测试库所有词的个数
dictionary={}
tagging={}
library=[]#存词库中词的序列
test_library=[]#存测试库中词序列
sentence_answer=[]#存每个测试句子的正确词性序列，以便计算正确率
test_words_num=0#表示测试库中总词数，为delta矩阵、phi矩阵的行数

A=[]#状态转移矩阵，n*n
B=[]#发射矩阵，n*m
Pi=[]#初始概率矩阵，1*n
num=[]# num[i]代表词性序号为i的词性在语料库中出现的次数，这是状态转移矩阵A、发射矩阵B每一项概率的分母
delta=[]#delta[k-1][n-1]表示读到测试库某句话第k个词时以序号n的词性结尾的所有路径中最大的概率
phi=[]#phi[k-1][n-1]表示某句话使得以词性序号n结尾概率最大的倒数第二个词性序号
path=[]#存储最优路径的编号

#计算该语料库的总行数，以确定需要读入多少行作为词典
f=open("123.txt")
flines=f.readlines()
numlines=len(flines)
readnumlines=numlines*0.8
print("该语料库一共%d行，需要读%d行"%(numlines,readnumlines))
f.close()

print("开始创建语料库...")
#遍历语料库文件，得到n、m、dictionary{}、tagging{}、library[[]]、line
f=open("123.txt")
for line in f:
    if rows>=readnumlines-1:
        break
    if len(line)!= 0:
        library.append([])
        line1=re.sub("[[]","",line)#去掉左中括号
        temp=line1.split("]")#以右中括号为界分出几个不包含左右中括号的列表temp
        #print(temp)
        for words in temp:#对于temp中的每个字符串，以空格分割，这样剩下的没有左右中括号，而nt是残留的
            words1=words.split()
            for words2 in words1:#words2为分出来的不包含第一个数字串、不重复、不包含]后边nt的“词/词性”字符串们
                if ('199801' not in words2) and len(words2) != 1 and len(words2) != 2  and (words2 not in dictionary):
                    #print(words2)
                    words2_list=words2.split('/')#将words2分开，左边是词，右边是词性
                    words3=re.sub("[A-Za-z0-9\{\}]","",words2_list[0])#去掉词中的拼音和大括号,赋值给words3
                    words4=words3+'/'+words2_list[1]
                    if words3 not in dictionary:
                        dictionary[words3] = m
                        m+=1
                    if words2_list[1] not in tagging:
                        tagging[words2_list[1]] = n
                        n+=1
                    library[rows].append(words4)
        rows+=1
f.close()


print("开始创建测试库...")
#开始读入测试库
rows2=0
f=open("123.txt")
i=0
for line in f:
    if i<readnumlines-1:
        i+=1
        continue
    if len(line)!= 0:
        test_library.append([])
        line1=re.sub("[[]","",line)#去掉左中括号
        temp=line1.split("]")#以右中括号为界分出几个不包含左右中括号的列表temp
        #print(temp)
        for words in temp:#对于temp中的每个字符串，以空格分割，这样剩下的没有左右中括号，而nt是残留的
            words1=words.split()
            for words2 in words1:#words2为分出来的不包含第一个数字串、不重复、不包含]后边nt的“词/词性”字符串们
                if ('199801' not in words2) and len(words2) != 1 and len(words2) != 2  and (words2 not in dictionary):
                    #print(words2)
                    words2_list=words2.split('/')#将words2分开，左边是词，右边是词性
                    words3=re.sub("[A-Za-z0-9\{\}]","",words2_list[0])#去掉词中的拼音和大括号,赋值给words3
                    words4=words3+'/'+words2_list[1]
                    test_library[rows2].append(words4)
                    test_words_num+=1
        rows2+=1
f.close()


print("开始初始化矩阵A,B,Pi,delta，phi...")
#初始化矩阵A、B、Pi、num、delta、phi，否则无法随机访问
m=len(dictionary)
n=len(tagging)


for i in range(n):
    A.append([])
    for j in range(n):
        A[i].append(0)

for i in range(n):
    B.append([])
    for j in range(m):
        B[i].append(0)

for i in range(n):
    Pi.append(0)
    num.append(0)

for i in range(test_words_num):
    delta.append([])
    phi.append([])
    for j in range(n):
        delta[i].append(0)
        phi[i].append(0)


print("开始统计矩阵A,B,Pi,delta,phi各项数据...")
#遍历一遍library，根据两个dict()类型的词库dictionary{}、词性库tagging{}，借助num和rows
#算出状态转移矩阵A、发射矩阵B、初始概率矩阵Pi

#统计状态转移矩阵A、发射矩阵B各个项的数据
for sentence in library:
    if len(sentence)!=0:
        x=0
        for group_lex in sentence[1:]:
            group_pre=sentence[x]
            pre_list=group_pre.split('/')
            lex_list=group_lex.split('/')
            i=tagging[pre_list[1]]
            j=tagging[lex_list[1]]
            p=dictionary[pre_list[0]]
            A[i][j]+=1#从状态i转移到状态j的次数
            B[i][p]+=1#状态i对应现象p的次数
            num[i]+=1#num[i]代表词性序号为i的词性在语料库中出现的次数，这是状态转移矩阵A、发射矩阵B每一项概率的分母
            x+=1
#计算最后一个词性的发射矩阵对应的值和出现的次数
        group_last=sentence[x]
        last_list=group_last.split('/')
        i=tagging[last_list[1]]
        p=dictionary[last_list[0]]
        B[i][p]+=1
        num[i]+=1
#统计初始概率矩阵Pi每一项的数据
        first_list=sentence[0].split('/')
        first_str=first_list[1]
        i=tagging[first_str]
        Pi[i]+=1


print("开始计算矩阵A,B,Pi,delta,phi各项概率...")
#开始计算矩阵A,B,Pi各项的概率
for i in range(n):
    for j in range(n):
        tempa=float(A[i][j]+0.01)/((num[i])+0.01*n)
        A[i][j]=float(tempa)

for i in range(n):
    for j in range(m):
        tempb=float(B[i][j]+0.00002)/((num[i])+0.00002*m)
        B[i][j]=float(tempb)
    tempp=float(Pi[i]/rows)
    Pi[i]=tempp


print("开始对测试库进行测试...")
#维特比算法开始
f2=open("result.txt","a")
new_tagging={v:k for k,v in tagging.items()}
now=1
for test_sentence in test_library:
    if len(test_sentence)!=0:
        sentence_answer=[]#每一行测试句子都进行初始化
        path=[]

        #print(test_sentence)

        words_list=test_sentence[0].split('/')
        sentence_answer.append(words_list[1])#将标准答案存在sentence_answer中

        #第一个词不需要转移矩阵，单独计算
        words = words_list[0]
        for i in range(n):
            if words in dictionary.keys():
                delta[0][i]=Pi[i]*B[i][dictionary[words]]
            else:
                delta[0][i] = Pi[i]*0.1
        #每一句的第二个词到最后一个词
        t=1
        for words_original in test_sentence[t:]:#对于一句话的每一个词
            words_list = words_original.split('/')
            sentence_answer.append(words_list[1])
            words = words_list[0]
            for i in range(n):#对于当前词对应每种词性，求对应此词性所有路径的最大值，共有n个，phi记录最大概率时前一个词性
                max_temp=max(delta[t-1][x]*A[x][i] for x in range(n))
                if words in dictionary.keys():
                    delta[t][i]=max_temp*B[i][dictionary[words]]
                else:
                    delta[t][i] = max_temp*0.1
                for x in range(n):
                    if delta[t-1][x]*A[x][i]==max_temp:
                        break
                    else:
                        x+=1
                phi[t][i]=x
            t+=1
        #上边的for循环分别算出了n个以词性i(i从0到n-1)结尾的最大概率，下面来算这n个概率中的最大概率，
        #即可求出整个句子对应的最大可能性的词性序列,再用phi矩阵回溯
        t-=1
        max_probability=max(delta[t][i] for i in range(n))
        for i in range(n):
            if delta[t][i]==max_probability:
                break
            else:
                i+=1
        #现在已经得到了最大概率词性路径的最后一个词性序号i，利用phi进行回溯，t-1对应test_sentence最后一个词的序号
        path.append(new_tagging[i])
        while t>0:
            x=phi[t][i]
            path.append(new_tagging[x])
            i=x
            t-=1
        path.reverse()

        current_correct=0
        for i in range(len(path)):
            if path[i]==sentence_answer[i]:
                current_correct+=1
            total+=1
        correct+=current_correct
        print("这是第%d行，共%d个词性，你计算对了%d个"%(now,len(sentence_answer),current_correct))
        f2.write("这是第%d行，共%d个词性，你计算对了%d个\n"%(now,len(sentence_answer),current_correct))
        now+=1
    #path里存的是词性
        print(path)
        if (len(path) != 0):
            for word in path[:-1]:
                f2.write(word)
                f2.write("/")
            f2.write(path[len(path) - 1])
            f2.write("\n")

        print(sentence_answer)
        if (len(sentence_answer) != 0):
            for word in sentence_answer[:-1]:
                f2.write(word)
                f2.write("/")
            f2.write(sentence_answer[len(sentence_answer) - 1])
            f2.write("\n")

        print("\n")
        f2.write("\n")


correct_rate=float(correct/total)
print("共%d个词性，你计算对了%d个，正确率为%f"%(total,correct,correct_rate))
f2.write("共%d个词性，你计算对了%d个，正确率为%f\n"%(total,correct,correct_rate))
endtime=datetime.datetime.now()
print("程序运行时间为%s"%(endtime-starttime))
f2.write("程序运行时间为%s\n"%(endtime-starttime))
f2.close()
print("Press any key to exit")
any=input()






























#if words3 not in dictionary:
    #dictionary[words3] = 1
#if words2_list[1] not in tagging:
    #tagging[words2_list[1]] = 1