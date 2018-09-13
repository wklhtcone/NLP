import datetime
starttime=datetime.datetime.now()
pos=[]#用于存所有positive库的词语
neg=[]#用于存所有negative库的词语
p1=[]#用于存一个句子各个词的(词|positive)
p2=[]#用于存一个句子各个词的(词|negative)
product1=1#一个句子属于positive的概率
product2=1#一个句子属于negative的概率
probability1=0#一个句子各个词的p(词|positive)
probability2=0#一个句子各个词的p(词|negative)
num=0#一行中的某个词在positive或者negative语料库中出现的次数
correct1=0#positive测试库中测试通过的句子总数
correct2=0#negative测试库中测试通过的句子总数
total1=0#positive测试库句子总数
total2=0#negative测试库句子总数
rate1=0#positive测试库的正确率
rate2=0#negative测试库的正确率
#计算该语料库的总行数，以确定需要读入多少行作为词典
f=open("rt-polarity.pos","rb")
flines=f.readlines()
numlines=len(flines)
readnumlines=numlines*0.8#每个库80%用于学习，20%用于测试
f.close()

#开始创建positive的语料库
f=open("rt-polarity.pos","rb")
i=1
for line in f:
    if i>readnumlines:
        break
    words_list=line.split()
    for word in words_list:
        pos.append(word)
    i+=1
print("共读入%d行作为positive的语料库"%(i-1))
f.close()

#开始创建negative的语料库
f=open("rt-polarity.neg","rb")
i=1
for line in f:
    if i>readnumlines:
        break
    words_list=line.split()
    for word in words_list:
        neg.append(word)
    i+=1
print("共读入%d行作为negative的语料库"%(i-1))
f.close()



#开始测试positive库
print("开始测试positive库")
f=open("rt-polarity.pos","rb")
f2=open("result.txt",'a')
f2.write("开始测试positive库\n")
i=1
row=1
for line in f:
    if i<=readnumlines:
        i+=1
        continue
    p1=[]
    p2=[]
    product1=1
    product2=1
    words_list=line.split()
    for word in words_list:
        num=pos.count(word)
        probability1=(num+1)/(len(pos)+len(words_list))
        p1.append(probability1)
        num=neg.count(word)
        probability2=(num+1)/(len(neg)+len(words_list))
        p2.append(probability2)

    for pro in p1:
        product1*=pro
    for pro in p2:
        product2*=pro
    if product1>product2:
        correct1+=1
        print("第%d行，这是positive样例，测为positive，测试成功"%(row))
        f2.write("第%d行，这是positive样例，测为positive，测试成功\n" % (row))
    else:
        print("第%d行，这是positive样例，测为negative，测试失败"%(row))
        f2.write("第%d行，这是positive样例，测为negative，测试失败\n" % (row))
    total1+=1
    row+=1
rate1=correct1/total1
print("positive库测试的准确率为%f"%(rate1))
f2.write("positive库测试的准确率为%f\n\n"%(rate1))
f.close()


#开始测试negative库
print("开始测试negative库")
f2.write("开始测试negative库\n")
f=open("rt-polarity.neg","rb")
i=1
row=1
for line in f:
    if i<=readnumlines:
        i+=1
        continue
    p1=[]
    p2=[]
    product1=1
    product2=1
    words_list=line.split()
    for word in words_list:
        num=pos.count(word)
        probability1=(num+1)/(len(pos)+len(words_list))
        p1.append(probability1)
        num=neg.count(word)
        probability2=(num+1)/(len(neg)+len(words_list))
        p2.append(probability2)

    for pro in p1:
        product1*=pro
    for pro in p2:
        product2*=pro
    if product1<product2:
        correct2+=1
        print("第%d行，这是negative样例，测为negative，测试成功"%(row))
        f2.write("第%d行，这是negative样例，测为negative，测试成功\n" % (row))
    else:
        print("第%d行，这是negative样例，测为positive，测试失败"%(row))
        f2.write("第%d行，这是negative样例，测为positive，测试失败\n" % (row))
    total2+=1
    row+=1
rate2=correct2/total2
print("negative库测试的准确率为%f"%(rate2))
f2.write("negative库测试的准确率为%f\n\n"%(rate2))
f.close()
rate=(correct1+correct2)/(total1+total2)
print("测试结果：")
f2.write("测试结果：\n")
print("positive库测试的准确率为%f，negative库测试的准确率为%f，两个库测试的总准确率为%f"%(rate1,rate2,rate))
f2.write("positive库测试的准确率为%f，negative库测试的准确率为%f，两个库测试的总准确率为%f\n"%(rate1,rate2,rate))
endtime=datetime.datetime.now()
print("程序运行时间%s"%(endtime-starttime))
f2.write("程序运行时间%s\n"%(endtime-starttime))
print("Press any key to exit")
f2.close()
any=input()






