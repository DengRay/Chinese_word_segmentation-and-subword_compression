# -*- coding:utf-8 -*-
import json
import os
import time
from lstm.lstm_net import LongShortTMNet
from lstm.processing import DataProcessing
from pickle import load
from bpe_finish import bpe

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

INIT_WEIGHT_WV_PATH = 'model/init_weight_wv.pickle'

VOCAB_DICT_PATH = 'dictionary/word2idx.pickle'
LABEL_DICT_PATH = 'dictionary/label_dict.pickle'
NUM_DICT_PATH = 'dictionary/num_dict.pickle'

# 全局加载词典
if os.path.exists(VOCAB_DICT_PATH):
    with open(VOCAB_DICT_PATH, 'rb') as f:
        vocab_dict = load(f)
    print("[INFO] The vocab_dict is load!")
else:
    raise Exception("[ERROR] The word2idx.pickle is not exist!")

if os.path.exists(LABEL_DICT_PATH):
    with open(LABEL_DICT_PATH, 'rb') as f:
        label_dict = load(f)
    print("[INFO] The label_dict is load!")
else:
    raise Exception("[ERROR] The label_dict.pickle is not exist!")

if os.path.exists(NUM_DICT_PATH):
    with open(NUM_DICT_PATH, 'rb') as f:
        num_dict = load(f)
    print("[INFO] The num_dict is load!")
else:
    raise Exception("[ERROR] The num_dict.pickle is not exist!")

# 全局加载模型
data_processing = DataProcessing()
lstm_net = LongShortTMNet()
lstm_net.model_load('lstm_model')

def get_cut_word():
    context = "研究生命科学 研究生命令本科生 我从马上下来 我马上下来 北京大学生喝进口红酒 在北京大学生活区喝进口红酒 从小学电脑 从小学毕业 美军中将竟公然说 新建地铁中将禁止商业摊点 这块地面积还真不小 地面积了厚厚的雪 让我们以爱心和平等来对待动物 阿美首脑会议将讨论巴以和平等问题 锌合金把手的相关求购信息 别把手伸进别人的口袋里 将信息技术应用于教学实践 信息技术应用于教学中的哪个方面 上级解除了他的职务 方程的解除了零以外还有 我们一起去故宫 一起恶性交通事故 我不想吃东西 你就不想想 各国有企业相继倒闭 各国有各国的困难 老人家身体不错 老人家中很干净 和服务必归还 技术和服务 他站起身 他起身去北京 问题的确定 这的确定不下来 结合成分 为人民工作 中国产品质量 原子结合成分子时 部分居民生活水平 治理解放大道路面积水 这样的人才能经受住考验 他俩儿谈恋爱是从头年元月开始的 在这些企业中国有企业有十个 结婚的和尚未结婚的"
    start_time = time.time()
    x_data = data_processing.predict_transform(context, vocab_dict)
    #print(x_data)
    predict_result = lstm_net.cut_word(x_data, context, label_dict, num_dict)
    print("predict: ",predict_result)
    end_time = time.time()
    print("Cost time is: ", end_time - start_time)
    return predict_result

if __name__ == '__main__':
    predict_result = get_cut_word()
    iteration_num = 10
    bpe(iteration_num,predict_result)