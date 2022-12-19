path1 = "corpus/my_msr.txt"
path2 = "corpus/my_msr_cl.txt"


def data_clean(path1,path2):
    kk=open(path2,'a')
    jg=open(path1,encoding = "gbk")
    temp = jg.read()
    #X,Y = ['\u0061','\u007a']
    X,Y = ['\u4e00','\u9fa5']
    for x_1 in temp:
        if X <= x_1 <= Y:
            kk.write(x_1)
        elif x_1 == " ":
            kk.write(x_1)
        elif x_1 == "\n":
            kk.write(x_1)
    kk.close
    jg.close
    
data_clean(path1,path2)