#!/usr/bin/python
#coding=utf-8

import BitVector
import cmath

#初始化时获取n个素数作为种子
def get_n_prime(n):

    def is_prime(x):
        for i in range(2,int(x*0.5)+1):
            if x%i == 0 :
                return False
        return True

    def get_prime(n):
        pri=[]
        i=5
        while len(pri)<n :
            if is_prime(i):
                pri.append(i)
            i+=1
        return pri
    return get_prime(1+n*5)[0:n*5:5]
    #返回对应的n个数字，结束

#哈希工具，用于处理字符串
#这里使用了bkdrhash的哈希算法
class SimpleHash:
    def __init__(self,cap,seed):
        self.cap = cap
        self.seed = seed

    def hash(self,str):
        ret = 0
        for ch in str:
            ret += self.seed * ret + ord(ch)
        return (self.cap-1) & ret

class BloomFilter:
    def __init__(self, error_rate, elementNum):
        print '初始化布隆过滤器,设计错误率 %.6f ,设计容量 %d' % (error_rate,elementNum)
        #计算所需要的bit数
        self.bit_num = -1 * elementNum * cmath.log(error_rate) / (cmath.log(2.0) * cmath.log(2.0))

        #计算位数组大小size
        self.BIT_SIZE = self.align_4byte(self.bit_num.real)

        #计算hash函数的个数 n
        self.hash_num = cmath.log(2) * self.BIT_SIZE / elementNum
        self.hash_num = int(self.hash_num.real) +1

        #分配内存
        self.bit_set = BitVector.BitVector(size=self.BIT_SIZE)

        #定义哈希种子
        self.seeds = get_n_prime(self.hash_num)
        print "Hash seeds =",self.seeds

        #根据种子创建函数
        self.hash_Func = []
        for seed in self.seeds:
            self.hash_Func.append(SimpleHash(self.BIT_SIZE, seed))
        #print len(self.hashFunc)

    #换算位数组大小
    def align_4byte(self, bit_num):
        num = int(bit_num / 32)
        num = 32 * (num + 1)
        return num

    #插入函数，将获取字符串在各个hash函数离散后的值并置1
    def insert(self,str):
        for f in self.hash_Func:
            pos = f.hash(str)
            self.bit_set[pos] = 1

    #查询函数，将被查询的字符串进行离散后的每一位进行查找
    def exist(self,str):
        for f in self.hash_Func:
            pos = f.hash(str)
            if self.bit_set[pos] == 0:
                return False
        return True

#测试用函数
def BloomTest():
    fd = open("urls.txt")
    bloomfilter = BloomFilter( 0.000001, 100000000)
    print 'size = %d,n = %d'%(bloomfilter.BIT_SIZE,bloomfilter.hash_num)
    while True:
        #url = raw_input()
        url = fd.readline()
        if cmp(url, 'exit') == 0: #如果输入字符串为exit表示结束
            break
        if bloomfilter.exist(url) == False:
            bloomfilter.insert(url)
        else:
            print 'url :%s has exist' % url

BloomTest()
