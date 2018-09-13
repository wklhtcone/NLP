import re
import datetime
starttime=datetime.datetime.now()
sentence=""#每行生成的句子
slist=[]#该行句子的正确分法
ylist=[]#该行句子你的分法
dictionary={}


yseg=0#该行你分成了多少词
ytotal=0#你分的所有行yseg相加
sseg=0#该行正确的分词个数
stotal=0#正确的所有行总词数相加
ycorrect=0#该行句子你分对的个数
total_correct=0#所有行的ycorrect相加
precision=0
recall=0
fmeasure=0
numlines=0
maxlen=8

#计算该语料库的总行数，以确定需要读入多少行作为词典
f=open("123.txt")
flines=f.readlines()
numlines=len(flines)
readnumlines=numlines*0.8
print("该语料库一共%d行，需要读%d行作为语料库，剩下的用于测试"%(numlines,readnumlines))
f.close()

#读入语料库的前80%行作为词典
f=open("123.txt")#wkl.txt是一个语料库
i=1
for line in f:
    if i>readnumlines:
        break
    words=line.split()#得到每行的单词以列表的形式存储
    if len(words)!= 0:
        del(words[0])#去掉第一个单词
    for temp1 in words:#对每个单词只要/左边的部分
        temp2=temp1.split('/')
        temp2[0] = re.sub("[A-Za-z0-9\{\}]", "", temp2[0])
        if temp2[0] not in dictionary:
            dictionary[temp2[0]]=1#将每行所有的词加入dictionary这个词典
    i+=1
print("在该语料库中共读入了%d行作为词典"%(i-1))

f.close()


f=open("123.txt")
f2=open("result.txt",'a')
i=1
rows=1
for line in f:
    #跳过前80%
    if i<=readnumlines:
        i+=1
        continue
    #每行都要进行初始化
    ylist=[]
    slist=[]
    ycorrect=0#该行句子你分对的个数
    yseg=0#该行你分成了多少词
    sseg=0#该行正确的分词个数

    #开始每行的处理
    print("这是第%d行:"%(rows))
    words=line.split()#得到每行的单词以列表的形式存储
    if len(words)!= 0:
        del(words[0])#去掉第一个单词
        for temp1 in words:#对每个单词只要/左边的部分
            temp2=temp1.split('/')
            temp2[0] = re.sub("[A-Za-z0-9\{\}]", "", temp2[0])
            slist.append(temp2[0])
            sentence+=temp2[0]#将该行的单词组成句子

        #开始对该行的句子进行逆向最大匹配算法（BMM）
        while len(sentence)>0:
            if len(sentence)>8:
                maxlen=8
            else:
                maxlen=len(sentence)
            while maxlen>0:
                seg=sentence[-maxlen:]#比如maxlen=4，就取句子的后4个字符组成一个词seg
                if seg in dictionary:#找到这个词
                     ylist.append(seg)#将seg加入到ylist列表中，即该行你分词的结果
                     sentence=sentence[:-maxlen]#去掉这maxlen长度已经分出来的词
                     break

                else:
                    maxlen=maxlen-1#长度减1，继续循环
            if maxlen==0:#sentence的最后一个字组成一个词的情况
                ylist.append(sentence[-1:])
                sentence=sentence[:-1]
        ylist.reverse()

        '''
        #开始计算该行的正确词数
        for lex in ylist:
            if slist.count(lex)!=0:
                ycorrect=ycorrect+1
        '''
        # 开始计算该行的正确词数(改进算法)
        p=0
        q=0
        m=0
        n=0
        while m<len(slist) and n<len(ylist):
            if(p==q):
                if(slist[m]==ylist[n]):
                    ycorrect+=1
                p+=len(slist[m])
                q+=len(ylist[n])
                m+=1
                n+=1
            elif p<q:
                p+=len(slist[m])
                m+=1
            else:
                q+=len(ylist[n])
                n+=1

        #开始统计
        yseg=len(ylist)#这一行你分了多少个
        sseg=len(slist)#这一行正确的分词个数
        ytotal+=yseg#你总共的分词个数
        stotal+=sseg#总共分词个数
        total_correct+=ycorrect#你分对的总数
        print("第%d行应分为%d个词，你分成了%d个词，分对了%d个词"%(rows,sseg,yseg,ycorrect))
        f2.write("第%d行应分为%d个词，你分成了%d个词，分对了%d个词\n"%(rows,sseg,yseg,ycorrect))


        print(slist)
        if(len(slist)!=0):
            for word in slist[:-1]:
                f2.write(word)
                f2.write("/")
            f2.write(slist[len(slist)-1])
            f2.write("\n")

        print(ylist)
        if (len(ylist) != 0):
            for word in ylist[:-1]:
                f2.write(word)
                f2.write("/")
            f2.write(ylist[len(ylist)-1])
            f2.write("\n")
        print("\n")
        f2.write("\n")
        rows+=1
f.close()


precision=total_correct/ytotal
recall=total_correct/stotal
fmeasure=2*precision*recall/(precision+recall)
print("应分为%d个词，你分成了%d个词，分对了%d个词"%(stotal,ytotal,total_correct))
f2.write("应分为%d个词，你分成了%d个词，分对了%d个词\n"%(stotal,ytotal,total_correct))
print("正确率为%f，召回率为%f，F-measure为%f"%(precision,recall,fmeasure))
f2.write("正确率为%f，召回率为%f，F-measure为%f\n"%(precision,recall,fmeasure))
endtime=datetime.datetime.now()
print("程序运行时间为%s"%(endtime-starttime))
f2.write("程序运行时间为%s\n"%(endtime-starttime))
f2.close()
print("Press any key to exit")
any=input()