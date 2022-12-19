from nltk.probability import FreqDist
from nltk.text import Text
import collections

def bpe(iteration_num,context_split):
    #context_split = ['low','lower','lower','newer']
    context_raw = []
    for i in context_split:
        for j in i:
            if j!='，'and j!='。':
                context_raw.append(j)
        context_raw.append("|") #词语划分符号
    #print(context_raw)

    text = Text(context_split)
    word_fre = FreqDist(text)
    chara = Text(context_raw)
    char_fre = FreqDist(chara)

    #print(list(char_fre.items()))
    #print(char_fre.get('l'))
    '''
    a=set()
    for word,freq in word_fre.items():
        for i in range(len(word)):
            a.add(word[i])
    print(a)
    '''
    for j in range(iteration_num):
        pairs =collections.defaultdict(int)
        for i in range(len(context_raw)-1):
            if context_raw[i+1] != '|'and context_raw[i] != '|':
                pairs[context_raw[i],context_raw[i+1]]+=1
        '''        
                    
        for word,freq in word_fre.items():
            #print(word)
            for i in range(len(word)-1):
                pairs[word[i],word[i+1]]+= freq
        '''
        #print(word_fre) 
        #print(pairs)
    
        best = max(pairs,key = pairs.get)
        fre=pairs.get(best)
        if fre == 1:
            print("Too many iterations")
            break
        #print(best)
        #print(fre)
        temp_1 = best[0]
        temp_2 = best[1]
        print("第{}次迭代，将{}与{}合并".format(j+1,temp_1,temp_2))
        for i in range(len(context_raw)-fre):
            if (context_raw[i] == temp_1) and (context_raw[i+1] == temp_2):
                context_raw[i]=temp_1 + temp_2
                context_raw.pop(i+1)

        #a.add(temp_1+temp_2) 
        #print(context_raw)

        char_fre[temp_1+temp_2] = fre
        if char_fre.get(temp_1) == fre:
            char_fre.pop(temp_1)
        if char_fre.get(temp_2) == fre:
            char_fre.pop(temp_2)
        print("这是子词压缩词典")  
        print(list(char_fre.items()))

    
if __name__ == '__main__':
    iteration_num = 10
    context_split = ['我', '是', '中国', '科学院', '大学', '的', '一', '名', '电子', '信息', '研究', '生，', '他', '也', '是', '中国', '科学院', '大学', '的', '一', '名', '研究', '生，', '他', '研究', '的', '是', '信息', '工程', '，', '我', '研究', '的', '是', '自然', '语言', '处理', '，', '即使', '他', '的', '语言', '天赋', '比', '我强']
    bpe(iteration_num,context_split)